from baseclasses.generics import StatedObject
from cardgroups import DeckCardGroup, BoardCardGroup, BurnCardGroup
from chips import PotChips
from copy import copy

class PokerHand(StatedObject):
    """docstring for PokerHand"""
    def __init__(self, handid, pokertable):
        super(PokerHand, self).__init__()
        self.states = [
            "postgame",
            "showdown",
            "riverbetting",
            "dealriver",
            "turnbetting",
            "dealturn",
            "flopbetting",
            "dealflop",
            "preflopbetting",
            "dealpocket",
            "pregame"
        ]

        self.pk = handid

        # Cards
        self.deck = DeckCardGroup()
        self.board = BoardCardGroup()
        self.burn = BurnCardGroup()

        # action Controls
        self.defaultactions = ["check", "fold", "bet", "call"]
        self.currentactions = []

        # Static Pot Controls
        self.bigblind = 0
        self.smallblind = 0

        # Dynamic Pot Controls
        self.minbet = 0 # changes with each bet
        self.callamount = 0

        #Pots
        # there needs to be a pot manager to see if we need to split a pot or something, just not there yet
        self.mainpot = PotChips()
        self.sides = []

        # Table
        self.table = pokertable

    def state_change(self):
        super(PokerHand, self).state_change()

    def pregame(self, dealerposition=0, bigblind=20, smallblind=10):
        self.state_change()
        self.bigblind = bigblind
        self.smallblind = smallblind
        self.minbet = bigblind
        self.callamount = bigblind
        self.table.set_button(dealerposition)
        self.table.assign_blinds()
        self.deck.shuffle()
        self.table.set_actor(self.table.smallposition)
        self.state_change()

    def deal_pocket(self):
        small = self.table.smallposition
        for x in range(0, len(self.table.active)*2):
            self.table.get_actor_as_player().deal_pocket_card(self.deck.pop_pocket())
            self.table.next_active_player()
        self.table.set_actor(self.table.bigposition)
        self.table.next_active_player()
        self.currentactions = copy(self.defaultactions)
        self.currentactions.remove("check")
        self.state_change()

    def action(self, details={}):
        success = False
        if details:
            actiontype = details['type']
            player = details['player']
            amount = details['amount']
            if actiontype == 'Fold':
                pass
            elif actiontype == 'Call':
                pass
            elif actiontype == 'Bet':
                pass
            elif actiontype == "Check":
                pass

        if success:
            self.table.next_active_player()
            return True
        return False


    def hand_status(self):
        return {
            "board":self.board.as_dict(),
            "table": self.table.as_dict(),
            "actor": self.table.get_actor_as_player().as_dict(),
            "actions": self.currentactions,
            "min_bet":self.minbet,
            "call_amount": self.callamount,
            "main_pot": self.mainpot.as_dict(),
            "side_pots": self.sides,
            "state": self.currentstate
        }