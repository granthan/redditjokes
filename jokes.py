import sys, time, csv, requests, json

def run_jokes():
    arguments_len = len(sys.argv)

    print("Example subreddits: jokes, dadjokes, puns")
    inp = input("Specify subreddit or type 'exit' to quit: ")
    
    if inp == 'exit':
        exit()

    joke_list = read_jokes_reddit(inp)

    if not joke_list:
        print("Invalid jokes subreddit\n")
        run_jokes()

    print_jokes(joke_list[0], joke_list[1])

    continue_read = read_input()
    curr_index = 2

    while curr_index < len(joke_list) and continue_read:
        print_jokes("\n" + joke_list[curr_index], joke_list[curr_index + 1])
        curr_index += 2
        if curr_index < len(joke_list):
            continue_read = read_input()

    print()
    if continue_read:
        print('End of jokes.')
    else:
        print('Ended due to user request.')

def print_jokes(prompt, punchline):
    print(prompt)
    time.sleep(2)
    print(punchline + "\n")

def read_input():
    while True:
        inp = input("Type 'next' for next joke, or 'exit' to quit: ")
        if inp == 'next':
            return True
        elif inp == 'exit':
            return False
        else:
            print("\n" + "I don't understand, please try again.")


def read_jokes_reddit(subreddit):
    reddit_json_link = "https://www.reddit.com/r/" + subreddit + ".json"
    reddit_request = requests.get(reddit_json_link, headers = {'User-agent': "Grant's joke bot 1.0"})
    parsed_jokes = json.loads(reddit_request.text)

    if 'data' not in parsed_jokes:
        print("Invalid jokes subreddit\n")
        run_jokes()

    jokes_list = parsed_jokes['data']['children']

    if not jokes_list:
        print("Invalid jokes subreddit\n")
        run_jokes()
    
    filtered_jokes = []
    
    for joke in jokes_list:
        over_18 = joke['data']['over_18']
        joke_title = joke['data']['title']
        punchline = joke['data']['selftext']
        is_question = joke_title.startswith(('Why', 'What', 'How')) and joke_title.endswith("?")
        if not over_18 and is_question and punchline:
            filtered_jokes.append(joke_title)
            filtered_jokes.append(punchline)
    return filtered_jokes


def read_jokes_csv(jokes_csv):
    jokes_list = []
    current_line = 1
    try:
        with open(jokes_csv) as jokes_file:
            jokes_reader = csv.reader(jokes_file, delimiter=',')
            for joke in jokes_reader:
                if len(joke) == 2:
                    prompt, punchline = joke[0], joke[1]
                    if not prompt or not punchline:
                        raise ValueError()
                    jokes_list.append(prompt)
                    jokes_list.append(punchline)
                else:
                    raise ValueError()
                current_line += 1
    except FileNotFoundError:
            print("File not found. Check the location or name of the CSV file and try again.")
            exit()
    except ValueError:
            print("All jokes in the specified CSV must be in pairs. Missing prompt or punchline detected at line %d." \
            % (current_line))
            exit()

    return jokes_list

run_jokes()
