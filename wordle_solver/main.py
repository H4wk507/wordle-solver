import json
from operator import itemgetter
from random import sample

NROWS = 6
NCOLS = 5


def read_json(fname: str) -> list[str]:
    with open(fname, "r") as f:
        return json.load(f)


def main() -> int:
    words = read_json("words.json")
    print("""Tutorial:
    Write a 5-letter string of b, y or g, where each letter
    is a color you got on wordle guess.""")
    WORD = ["" for _ in range(NCOLS)]
    while True:
        word = sample(words, 1)[0]
        print(f"guess: {word}")
        print(f"Words left: {len(words)}")
        inp = input()
        assert len(inp) == NCOLS
        black, yellow, green = [], [], []
        for idx, (color, letter) in enumerate(zip(inp, word)):
            assert color.lower() in "byg"
            match color.lower():
                case "b":
                    black.append(letter)
                case "y":
                    yellow.append((idx, letter))
                case "g":
                    green.append((idx, letter))
        for idx, letter in green:
            WORD[idx] = letter
        filtered_words = []
        for word in words:
            match = all(word[idx] == letter for idx, letter in green)
            if match:
                filtered_words.append(word)
        words = filtered_words[:]
        filtered_words = []
        free_indices = [idx for idx, letter in enumerate(WORD) if letter == ""]
        if len(black) > 0:
            for word in words:
                match = not any(
                    b in itemgetter(*[i for i in free_indices])(word)
                    for b in black
                )
                if match:
                    filtered_words.append(word)
        words = filtered_words[:]
        filtered_words = []
        if len(yellow) > 0:
            for word in words:
                match = all(
                    word[idx] != letter
                    and letter in itemgetter(*[i for i in free_indices])(word)
                    for idx, letter in yellow
                )
                if match:
                    filtered_words.append(word)
            words = filtered_words[:]
        if len(words) == 1:
            print(f"Guess: {words[0]}")
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
