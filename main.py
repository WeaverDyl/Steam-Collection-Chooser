from pathlib import Path
import requests, json, random, vdf
from steam import steamid

# TODO: Exception handling
# TODO: Comment
# TODO: Cleanup

def get_user_list():
    # Gets a list of users found on the machine
    users = []

    # Make work with other OS's
    path = Path('C:\\Program Files (x86)\\Steam\\userdata')
    
    # Add each directory name to the list of users
    for user_id in path.iterdir():
        if user_id.is_dir():
            users.append(user_id.name)

    return users

def ask_user_id(users):
    # Ask the user which user to select from the get_user_list() func
    chosen_user = None # Set up
    user_map = {} # Stores user_id as value and option_id as key
    option_id = 1

    # Assign each user a unique option_id
    for user in users:
        user_map[str(option_id)] = user
        option_id += 1
    
    # Ask user for selection, if selection not valid, ask again
    while chosen_user not in list(user_map.values()):
        print("Please choose a user:")
        
        for option_id, user in user_map.items():
            steam_id = steamid.make_steam64(user) # Convert SteamID3
            get_username_from_id(steam_id)
            steam_username = get_username_from_id(steam_id)
            print(f"{option_id}. '{steam_username}'")

        chosen_option_id = input() # Allow user input
        
        try:
            chosen_user = user_map[chosen_option_id]
        except KeyError:
            continue

    return chosen_user

def get_username_from_id(steam_id):
    API_KEY = ''
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={steam_id}'

    res = requests.get(url)
    return json.loads(res.text)['response']['players'][0]['personaname']

def get_sharedconfig(user_id):
    # Return a reference to the selected user's sharedconfig file
    path = Path(f'C:\\Program Files (x86)\\Steam\\userdata\\{user_id}\\7\\remote')
    f = vdf.load(open(f'{path}\\sharedconfig.vdf'))
    return f

def get_collections(sharedconfig):
    base = sharedconfig['UserLocalConfigStore']['Software']['Valve']['Steam']['Apps']
    collections = {}

    for game_id, game_info in base.items():
        try:
            for collection in game_info['tags'].values():
                if collection in collections.keys():
                    collections[collection].append(game_id)
                else:
                    collections[collection] = [game_id]
        except KeyError:
            # Game isn't in any collections
            continue

    return collections

def ask_user_collection(collections):
    # Ask the user which user to select from the get_collections() func
    chosen_collection = None # Set up
    collection_map = {} # Stores user_id as value and option_id as key
    option_id = 1

    # Assign each user a unique option_id
    for collection in collections.keys():
        collection_map[str(option_id)] = collection
        option_id += 1
    
    # Ask user for selection, if selection not valid, ask again
    while chosen_collection not in list(collection_map.values()):
        print("Please choose a collection:")
        
        for option_id, collection in collection_map.items():
            print(f"{option_id}. '{collection}'")

        chosen_option_id = input() # Allow user input
        
        try:
            chosen_collection = collection_map[chosen_option_id]
        except KeyError:
            continue

    return collections[chosen_collection]

def choose_game(collection, tries):
    # Choose a random game from the collection

    # Sometimes games are removed from Steam, etc... so we can't access the
    # game's name given it's ID.
    if tries == 0:
        print("Multiple failures. Try a different collection, or try again later.")
        return

    random_gameid = random.choice(collection)
    url = f'https://store.steampowered.com/api/appdetails/?appids={random_gameid}'
    res = requests.get(url)

    try:
        game_name = json.loads(res.text)[f'{random_gameid}']['data']['name']
        print(f'You should play {game_name}!')
    except KeyError:
        choose_game(collection, tries - 1)


all_users = get_user_list() # All users
chosen_user = ask_user_id(all_users) # Ask which user to select a game for
sharedconfig = get_sharedconfig(chosen_user) # Reference to sharedconfig

print() # Leave a space between user and collection text

all_collections = get_collections(sharedconfig) # List of all game collections
chosen_collection = ask_user_collection(all_collections) # The selected collection

print() # Leave a space between collection and chosen game text

choose_game(chosen_collection, 5) # Pick a random game and tell the user what it is