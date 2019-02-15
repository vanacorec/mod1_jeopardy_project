#j-archive is fairly consistent, we didn't implement the final jeopardy round to save time but it could be easily implemented
rounds = ["jeopardy_round", "double_jeopardy_round"]
#this comes into play during the actual parsing, but because we generated a list of show_ids, some of which don't point
# to actual games, I added a correct urls list to speed up parsing in case you want to run the scraper again
correct_url = []
#gets all the categories, seperated by jeopardy round, we use this to assign each clue to the correct category
def get_categories(jeopardy_round_id, game_soup):

    category_list = []

    jeopardy_round = game_soup.find("div", id = jeopardy_round_id)
    jeopardy_round_name = jeopardy_round.find("h2").get_text()
    categories = jeopardy_round.find_all("td", class_ = "category_name")
    for category in categories:
        category_list.append(category.get_text())

    return category_list
#gets the show number and date
def get_show_number_date(game_soup):
    number_date_string = game_soup.find('h1').get_text()
    split_string = number_date_string.split('-')
    number = split_string[0].strip()
    date = split_string[1].strip()

    return number, date
# gets all of the players in the game from the soup
def get_players(game_soup):
        contestants_list = []
        contestants = game_soup.find_all("p", class_ = "contestants")
        for contestant in contestants:
            contestants_list.append(contestant.find('a').get_text())
        return contestants_list
#retrieves all of our clue data and save it to it's own dictionary, adds Nones for exception cases
def get_clue_data(jeopardy_round_id, categories, game_soup):

    jeopardy_round = game_soup.find("div", id = jeopardy_round_id)
    clue_list_of_dictionaries = []
    clues = jeopardy_round.find_all("td", class_ = "clue")
    for clue in clues:
        clue_dictionary = {}


        # get clue text
        clue_text = clue.find("td", class_ = "clue_text")
        if clue_text != None:
            clue_dictionary["clue_text"] = clue_text.get_text()
        else:
            clue_dictionary["clue_text"] = None


        # get clue value
        clue_value = clue.find("td", class_ = "clue_value")
        if clue_value == None:
            daily_double_value = clue.find("td", class_ = "clue_value_daily_double")
            if daily_double_value == None:
                clue_dictionary["clue_value"] = daily_double_value
            else:
                clue_dictionary["clue_value"] = daily_double_value.get_text()
        else:
            clue_dictionary["clue_value"] = clue_value.get_text()


        #get clue id
        clue_id = clue.find("td", class_ = "clue_unstuck")
        if clue_id != None:
            clue_dictionary["clue_id"] = clue_id.get("id")

            clue_dictionary["category"] = get_category(categories, clue_id.get("id"))
        #get clue answer, answerer, and correct/incorrect value
        mouseover = clue.find("div", onmouseover=True)
        if mouseover != None:
            answer_string = BeautifulSoup(clue.find("div", onmouseover=True).get("onmouseover"))
            clue_dictionary['clue_answer'] = answer_string.find("em", class_ = "correct_response").get_text()
            if answer_string.find("td", class_ = "right") == None:
                clue_dictionary['clue_answerer'] =  answer_string.find('td', class_ = 'wrong').get_text()
                clue_dictionary['Answerer Correct?'] = False
            else:
                clue_dictionary['clue_answerer'] = answer_string.find("td", class_ = "right").get_text()
                clue_dictionary['Answerer Correct?'] = True
        else:
            clue_dictionary['clue_answer'] = None
            clue_dictionary['clue_answerer'] = None


        clue_list_of_dictionaries.append(clue_dictionary)

    return clue_list_of_dictionaries
# assigns correct category value to each clue
def get_category(categories, clue_id):
    return categories[int(clue_id[-9]) - 1]
#gets the score of the different rounds of the game, this could be expanded to account for games with tiebreakers
#or contestant changes
def get_final_score(game_soup):
    final_results = {}
    results = game_soup.find_all("td", class_ = "score_positive")
    result_list = []
    for result in results:
        result_list.append(result.get_text())

    names_list = []
    names = game_soup.find_all("td", class_ = "score_player_nickname")
    for name in names:
        names_list.append(name.get_text())

    if len(result_list) != 15:
        return None
    else:
        final_results[names_list[0]] = [result_list[0], result_list[3], result_list[6], result_list[9], result_list[12]]
        final_results[names_list[1]] = [result_list[1], result_list[4], result_list[7], result_list[10], result_list[13]]
        final_results[names_list[2]] = [result_list[2], result_list[5], result_list[8], result_list[11], result_list[14]]
    return final_results
#our function for parsing the games, game_list is a list of game_urls, puts each game dictionary into a larger dictionary
def parse_games(game_list):
    games = {}
    n = 0
    for game in game_list:
        try: #we ran a try/except/continue loop because we weren't sure of all of the urls that pointed to actual games
            game_url = game
            game_page = requests.get(game_url)
            game_soup = BeautifulSoup(game_page.content, 'html.parser')
            show_id, date = get_show_number_date(game_soup)
            games[show_id] = parse_game(game_soup)
            correct_url.append(game)#this will append the url to the correct_url list if it hits on a game that contains data
            n += 1                  # the var n and print statements were just added so we could track progress
            print(n)
        except:
            n += 1
            print(f'error! {n}')
            continue
    return games

def parse_game(game_soup): #this builds the individual game dictionary based on our functions defined above
    show_id, date = get_show_number_date(game_soup)
    game_id = {}
    game_id['Date'] = date
    rounds = ["jeopardy_round", "double_jeopardy_round"]
    game_id['Players'] = get_players(game_soup)
    for a_round in rounds:
        game_id[a_round] = get_clue_data(a_round, get_categories(a_round, game_soup), game_soup)
    game_id['results'] = get_final_score(game_soup)

    return game_id
