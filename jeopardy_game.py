

answer_list = []
value_list = []
contestant_list = {}

def get_random_question():
    x = np.random.randint(0,368630)
    if big_df.loc[x]['clue_answer'] != None:
        answer_list.append(big_df.loc[x]['clue_answer'])
        value_list.append(big_df.loc[x]['int_values'])
        return big_df.loc[x]['clue_text'],big_df.loc[x]['category']
    else:
        return "Please try again!"
def guess(Player,Guess):
    if Player not in contestant_list.keys():
        contestant_list[Player] = 0
        x = contestant_list[Player]
        if Guess == answer_list[-1]:
            contestant_list[Player] +=  value_list[-1]
            return f"Correct! You've won {value_list[-1]}"
        else:
            return "Wrong answer!"
    if Player in contestant_list.keys():
        if Guess == answer_list[-1]:
            x = contestant_list[Player]
            contestant_list[Player] +=  value_list[-1]
            return f"Correct! You've won {value_list[-1]}"
        else:
            return "Wrong answer!"
def new_game():
    answer_list = []
    value_list = []
    contestant_list = {}


plt.figure(figsize=(20,10))
plt.bar(np.arange(len(contestant_list.values())),contestant_list.values(),align="center",alpha=0.5)
plt.xticks(np.arange(len(contestant_list.keys())),contestant_list.keys(),rotation = 90)
plt.xlabel("Player")
plt.ylabel("Score")
plt.title("Jeopardy Scoreboard")
