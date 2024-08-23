def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = word_file.readlines()
    for i in range(len(valid_words)):
        valid_words[i] = valid_words[i].strip()

    return valid_words


def encrypt(message, code):
    new_message = ''
    list_of_words = load_words()
    for word in message.split():
        if word.lower() in list_of_words:
            index = list_of_words.index(word.lower())
            new_index = index + code
            new_message += list_of_words[new_index]
            new_message += ' '
        else:
            new_message += word
            new_message += ' '
    return new_message
