from pathlib import Path
from steamfiles import appinfo

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
        
        for user, key_mapping in user_map.items():
            print(f"{user}. '{key_mapping}'")

        chosen_key_mapping = input() # Allow user input
        
        try:
            chosen_user = user_map[chosen_key_mapping]
        except KeyError:
            continue

    return chosen_user

def get_sharedconfig(user_id):
    # Given a user, return the sharedconfig file located at
    # \user\7\remote\sharedconfig.vdf

    # this means that we'll always have a reference to the file
    # and don't need to load it multiple times
    pass

def get_collections(sharedconfig):
    # Get a list of all of the collections in the sharedconfig file
    pass

def ask_user_collection(collections):
    # ask which collection to choose a game from
    pass

def choose_game(collection):
    # Choose a random AppID and convert it to a readable title
    # and print it out to the user
    pass


all_users = get_user_list() # All users
chosen_user = ask_user_id(all_users) # Ask which user to select a game for

# sharedconfig = get_sharedconfig(chosen_user) # Reference to sharedconfig

# all_collections = get_collections(sharedconfig) # List of all game collections
# chosen_collection = ask_user_collection(all_collections) # The selected collection

# choose_game(chosen_collection) # Pick a random game and tell the user what it is

# TODO
# - can easily just make a function to choose from a python list
#   instead of having multiple functions (ask_user_id, ask_user_collection)
#   and just print a "choose a user"/"choose a collection" above the call