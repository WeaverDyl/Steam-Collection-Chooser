def get_user_list():
    # Get all users in C:\Program Files (x86)\Steam\userdata\
    # Make it work os-agnostically
    pass

def get_sharedconfig(user):
    # Given a user, return the sharedconfig file located at
    # \user\7\remote\sharedconfig.vdf

    # this means that we'll always have a reference to the file
    # and don't need to load it multiple times
    pass

def get_collections(sharedconfig):
    # Get a list of all of the collections in the sharedconfig file
    pass

def ask_user_id(users):
    # Ask the user which user to select from the get_user_list() func
    pass

def ask_user_collection(collections):
    # ask which collection to choose a game from
    pass

def choose_game(collection):
    # Choose a random AppID and convert it to a readable title
    # and print it out to the user
    pass


all_users = get_user_list() # All users
chosen_user = ask_user_id() # Ask which user to select a game for

sharedconfig = get_sharedconfig(chosen_user)

all_collections = get_collections(sharedconfig)
chosen_collection = ask_user_collection(all_collections)

choose_game(chosen_collection)

# TODO
# - can easily just make a function to choose from a python list
#   instead of having multiple functions (ask_user_id, ask_user_collection)
#   and just print a "choose a user"/"choose a collection" above the call