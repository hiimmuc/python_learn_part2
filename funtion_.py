def fizz_buzz(number):
    if (number % 5 == 0) and (number % 3 == 0):
        return "Fizz Buzz"
    if number % 3 == 0:
        return "Fizz"
    if number % 5 == 0:
        return "Buzz"
    return f"{number}"


def emoji_converter(sentence_):
    words = sentence_.split(" ")
    emoji_collection = {
        ":)": " 😊",
        ":D": " 😃",
        ":(": " ☹",
        ":o": " 😯"
    }
    output = ""
    for word in words:
        output += f" {emoji_collection.get(word, word)}"
    return output
