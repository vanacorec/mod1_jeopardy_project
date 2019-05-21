def json_to_games_df(json_dict):
    game_info = []
    for game in json_dict:
        show_id = game
        for key in json_dict[game]:
            date = json_dict[game]["Date"]
            players = json_dict[game]["Players"]
            results = json_dict[game]["results"]


        game_info.append({"Show_IDs": show_id, "Date": date, "Players" : players, "Results" : results})
    
    return pd.DataFrame(game_info)    

def json_to_clues_df(json_dict):
    

    all_clues = []
    for game in json_dict:
        show_id = game
        for clue in json_dict[game]['jeopardy_round']:

            clue_text = clue['clue_text']
            clue_answer = clue['clue_answer']
            clue_answerer = clue['clue_answerer']
            clue_value = clue['clue_value']

            try:
                answerer_correct = clue['Answerer Correct?']
            except:
                answerer_correct = None

            try: 
                category = clue['category']
            except:
                category = None

            try:
                clue_id = clue['clue_id'] 
            except:
                clue_id = None

            all_clues.append({"show_id": show_id, "round" : 'jeopardy_round', 'category': category, "clue_id": clue_id, "clue_text": clue_text, "answerer": clue_answerer, 'clue_value' : clue_value, 'clue_answer': clue_answer})

        for clue in json_dict[game]['double_jeopardy_round']:
            clue_text = clue['clue_text']
            clue_answer = clue['clue_answer']
            clue_answerer = clue['clue_answerer']
            clue_value = clue['clue_value']

            try:
                answerer_correct = clue['Answerer Correct?']
            except:
                answerer_correct = None

            try: 
                category = clue['category']
            except:
                category = None

            try:
                clue_id = clue['clue_id'] 
            except:
                clue_id = None

            all_clues.append({"show_id": show_id, "round" : 'double_jeopardy_round', 'category': category, "clue_id": clue_id, "clue_text": clue_text, "answerer": clue_answerer, 'clue_value' : clue_value, 'clue_answer': clue_answer })  

    return pd.DataFrame(all_clues)

def get_datetime_obj(date_string):
    return datetime.datetime.strptime(date_string, '%A, %B %d, %Y')

