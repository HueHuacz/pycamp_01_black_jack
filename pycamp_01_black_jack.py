""" Symulator gry w Blak Jack - Oczko """

from random import shuffle
from time import sleep
from sys import exit as sysexit


class Card:
    """ Klasa definiująca pojedynczą kartę """
    # posible_colours = ['pik', 'kier', 'trefl', 'karo']
    posible_colours = ['♠', '♥', '♣', '♦']
    # posible_ranks = [*range(2, 11, 1), 'walet', 'dama', 'król', 'as']
    posible_ranks = [*range(2, 11, 1), 'W', 'D', 'K', 'AS']

    def __init__(self, colour, rank):
        """ Inicjator objektu karta, który posiada kolor i range """
        self.colour = colour
        self.rank = rank

    def __str__(self):
        """ Odwzorowanie obiektu """
        return f'[{self.colour}-{self.rank}-{self.colour}]'


class Deck:
    """ Klasa definiująca talię, która jest listą wszystkich kart """
    def __init__(self):
        """ Inicjator objektu talia, który posiada elementy typu karta """
        self.deck = [Card(i, j) for i in Card.posible_colours for j in Card.posible_ranks]

    def shuffle_cards(self):
        """ Funkcja tasująca karty w talii """
        shuffle(self.deck)

    def give_card(self):
        """ Funkcja wystawiająca jedną kartę z talii """
        return self.deck.pop(0)


class Player:
    """ Klasa definiująca rękę gracza, która jest listą jego kart """
    def __init__(self):
        """ Inicjator objektu ręka, który posiada elementy typu karta """
        self.player_cards = []
        self.value = int

    def __str__(self):
        """ Odwzorowanie obiektu """
        player_cards = ' '.join(map(str, self.player_cards))
        return player_cards

    def take_card(self, one_card):
        """ Funkcja wstawiająca jedną kartę do ręki gracz """
        self.player_cards.append(one_card)
        self._get_value()

    def _get_value(self):
        """ Funkcja obliczająca wartość punktową ręki gracz """
        self.value = 0
        for i in self.player_cards:
            if isinstance(i.rank, int):
                self.value += i.rank
            elif i.rank in ('W', 'D', 'K'):
                self.value += 10
            elif i.rank == 'AS':
                self.value += 11
                if self.value > 21:
                    self.value -= 10
        return self.value


class BlackJack:
    """ Klasa definiująca przebieg rozgrywki """
    def __init__(self):
        """ Inicjator objektu gra, który posiada talię i ręce poszczególnych graczy"""
        print('\n\t--- BLACK JACK ---')
        self.bj_deck = Deck()
        self.bj_deck.shuffle_cards()
        self.croupier = Player()
        self.human = Player()

    def _starter_hand(self):
        """ Funkcja odpowiedzialna za pierwsze rozdanie """
        amount_of_aces = 0
        for _ in range(2):
            one_card_from_deck = self.bj_deck.give_card()
            self.human.take_card(one_card_from_deck)
            if one_card_from_deck.rank == 'AS':
                amount_of_aces += 1
            one_card_from_deck = self.bj_deck.give_card()
            self.croupier.take_card(one_card_from_deck)

        print(f'\nTwoje karty: {self.human}\nIch wartość: {self.human.value}')
        print(f'\nKarty croupiera: [****] {one_card_from_deck} ')

        if amount_of_aces == 2:
            raise TwoAses('\nDWA ASY! WYGRYWASZ!')

    def _human_move(self):
        """ Funkcja odpowiedzialna za ruch gracza """
        human_choise = None
        # while human_choise != 0:
        while human_choise not in ('p', 'P', 'pass', 'Pass', 'PASS', 0):
            # print('\nCo chcesz zrobić?\n 1: Dobierz kartę\n 0: Pass')
            print('\nCo chcesz zrobić? [D]obierasz kartę czy [P]asujesz?')
            # if (human_choise := int(input('Twój wybór: '))) != 0:
            if (human_choise := input('Twój wybór: ')) not in ('p', 'P', 'pass', 'Pass', 'PASS', 0):
                one_card_from_deck = self.bj_deck.give_card()
                self.human.take_card(one_card_from_deck)
                print(f'\nTwoje karty: {self.human}\nIch wartość: {self.human.value}')
                if self.human.value > 21:
                    raise Exceeded21('\n\t--- Przekroczyłeś 21! PRZEGRYWASZ! ---\n')

    def _croupier_move(self):
        """ Funkcja odpowiedzialna za ruch krupiera"""
        print(f'\nRuch krupiera!\nJego karty: {self.croupier}\nIch wartość: {self.croupier.value} ')
        while self.croupier.value < 17:
            print('\nKrupier dobiera karty...')
            sleep(1)
            one_card_from_deck = self.bj_deck.give_card()
            self.croupier.take_card(one_card_from_deck)
            print(f'Jego karty: {self.croupier}\nIch wartość: {self.croupier.value} ')
            sleep(1)
        if self.croupier.value > 21:
            raise Exceeded21('\n\t--- Krupier przekroczył 21! WYGRYWASZ! ---\n')

    def _compare_value(self):
        """ Funkcja wyłania zwycięzcę gry poprzez powrównanie wartości rąk graczy  """
        if self.human.value > self.croupier.value:
            print('\n\t--- Koniec gry! WYGRAŁEŚ! ---')
        elif self.human.value < self.croupier.value:
            print('\n\t--- Koniec gry! PRZEGRAŁEŚ! ---')
        elif self.human.value == self.croupier.value:
            print('\n\t--- Koniec gry! REMIS! ---')
        print(f'\tMiałeś {self.human.value} punktów')
        print(f'\tKrupier miał {self.croupier.value} punktów')

    def lets_play(self):
        """ Funkcja odpowiedzialna za kolejność elementów rozgrywki """
        try:
            self._starter_hand()
        except TwoAses as exception:
            sysexit(exception)
        try:
            self._human_move()
        except Exceeded21 as exception:
            sysexit(exception)
        try:
            self._croupier_move()
        except Exceeded21 as exception:
            sysexit(exception)
        self._compare_value()
        print('')


class Exceeded21(Exception):
    """ Klasa wyjątku obsługującego sytuację gdy któryś z graczy przekroczy 21 punktów """


class TwoAses(Exception):
    """ Klasa wyjątku obsługującego sytuację gdy gracz otrzyma dwa asy w pierwszym rozdaniu """


if __name__ == '__main__':

    game = BlackJack()
    game.lets_play()
