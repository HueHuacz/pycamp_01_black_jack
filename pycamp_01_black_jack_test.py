""" Skrypt do testowania """

from pycamp_01_black_jack import Card, Deck, Player


def test_init_card():
    test_card = Card('♠', 'AS')
    assert test_card.colour == '♠'
    assert test_card.rank == 'AS'


def test_str_card():
    card = Card('♠', 'AS')
    assert str(card) == '[♠-AS-♠]'


def test_init_deck():
    test_deck = Deck()
    assert len(test_deck.deck) == 52
    for i in ['♠', '♥', '♣', '♦']:
        assert len([card for card in test_deck.deck if i in card.colour]) == 13


def test_shuffle_cards():
    test_deck_v1 = Deck()
    test_deck_v2 = Deck()
    test_deck_v2.shuffle_cards()
    assert len(test_deck_v1.deck) == len(test_deck_v2.deck)
    assert any([str(test_deck_v1.deck[i]) != str(test_deck_v2.deck[i]) for i in range(52)])


def test_give_card():
    test_deck = Deck()
    check_first_card_from_deck = str(test_deck.deck[0])
    first_card_from_deck = test_deck.give_card()
    assert str(first_card_from_deck) == check_first_card_from_deck


def test_init_player():
    test_player = Player()
    assert test_player.player_cards == []


def test_take_card_and_get_value():
    test_player = Player()
    test_card = Card('♣', 'K')
    test_player.take_card(test_card)
    assert len(test_player.player_cards) == 1
    assert test_player.value == 10

# TODO: testy klasy BlackJack


def test():
    pass
