from game.data import PUZZLE

### Get all the words from the dictionary data into a single list ###
def get_all_words():

    words = []
    for category in PUZZLE.values():
        words.extend(category)
    return words


### Return the category of a word if it belongs to that category
def find_category(word):

    for category_name, words in PUZZLE.items():
        if word in words:
            return category_name
    return None
### Send 4 words(our selection), check the category for all 4 words and store them in a set. If there
### is more than category then the seletion is not correct
def check_selection(selection):

    categories = set()

    for word in selection:
        category = find_category(word)
        if category is None:
            return False
        categories.add(category)

    return len(categories) == 1

