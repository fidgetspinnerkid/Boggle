import Boggle


def test_roll_boggle_die_length_and_content():
    letters = Boggle.roll_boggle_die()
    assert len(letters) == 16
    assert all(len(c) == 1 and c.isalpha() for c in letters)


def test_order_letters_prints_board(capsys):
    letters = list('ABCDEFGHIJKLMNOP')
    Boggle.order_letters(letters)
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == ['A B C D', 'E F G H', 'I J K L', 'M N O P']


def test_find_score_values():
    words = ['cat', 'dogs', 'apple', 'carpet', 'monkeys', 'elephant']
    expected = [1, 1, 2, 3, 5, 11]
    assert Boggle.find_score(words) == expected


def test_spot_adjacent():
    assert Boggle.spot_adjacent(1, 2)
    assert Boggle.spot_adjacent(1, 6)
    assert not Boggle.spot_adjacent(1, 3)


def test_index_letter_multiple():
    grid = list('ABCDABCDABCDABCD')
    result = Boggle.index_letter('A', grid)
    assert result == [0, 4, 8, 12]
    assert grid == list('ABCDABCDABCDABCD')
    assert Boggle.index_letter('Z', grid) == -1


def test_valid_path():
    assert Boggle.valid_path([0, 1, 2])
    assert not Boggle.valid_path([0, 2])
    assert not Boggle.valid_path([0, 0])


def test_word_in_grid_found_and_not_found():
    board = ['C', 'A', 'T', 'D',
             'D', 'O', 'G', 'S',
             'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q']
    assert Boggle.word_in_grid('CAT', board[:])
    assert Boggle.word_in_grid('DOG', board[:])
    assert Boggle.word_in_grid('DOGS', board[:])
    assert not Boggle.word_in_grid('FISH', board[:])


def test_in_list(monkeypatch):
    monkeypatch.setattr(Boggle, 'words_set', frozenset({'cat', 'dog', 'dogs'}))
    assert Boggle.in_list('cat')
    assert not Boggle.in_list('bird')


def test_all_valid_words_and_find_longest(monkeypatch):
    dictionary = ['cat', 'dog', 'dogs', 'bird', 'fish']
    monkeypatch.setattr(Boggle, 'words_set', frozenset(dictionary))
    monkeypatch.setattr(Boggle, 'words_lst', dictionary)
    board = ['C', 'A', 'T', 'D',
             'D', 'O', 'G', 'S',
             'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q']
    words = Boggle.all_valid_words(board[:])
    assert words == ['cat', 'dog', 'dogs']
    longest = Boggle.find_longest_word(board[:])
    assert longest == 'dogs'
