# Description: This program will act as a board game that two-players can play. The board will be checkerboard style
# and either player can start the game, each player can make a single move, multiple move, or reserve move.
# The game will have a class called FocusGame for playing the game, and this class contains the game state,
# as well as the methods to play the game. The program also has methods that contain information about each player,
# the locations of the stack within the game, information about changing of turns, moving stacks, validity,
# and the player's move. Additionally, the rules of this game are that the players can alter a stack
# only if the highest piece on top of the stack belongs to them.
# When a stack happens to be on top of another stack, then the two stacks can then be combined,
# if the new stack has greater than 5 pieces, then the pieces are take out from the bottom to get it
# to 5. If the player's piece is take out, then it is kept and has to be on the board later
# instead of removing the stack. If the opponent's piece is taken out, then it is considered captured.
# A player will win the game if they are the last player that is able to move a stack.
# CS 162 Portfolio Project


from pprint import pprint


class FocusGame:
    """
    This class will be for playing the game.
    This class contains the game state, as well as the methods to play the game.
    """

    def __init__(self, player_1, player_2):
        """
        This method will take two tuples, and both must contain the name of a player, and the color
        that player is playing. For example ('PlayerA', 'R'), ('PlayerB','G').

        Initialize game board

        """
        # ------------------------------------------------------------
        # Set up the player data storage
        # ------------------------------------------------------------
        # both players data will be stored in a list containing two dictionaries
        # Both player dicts, should look like the following
        # {
        #    "name": "PlayerA",
        #    "color": "R",
        #    "reserved": 0,
        #    "captured": 0
        # }
        self._players = [
            {
                "name": player_1[0],
                "color": player_1[1],
                "reserved": 0,
                "captured": 0
            },
            {
                "name": player_2[0],
                "color": player_2[1],
                "reserved": 0,
                "captured": 0

            }
        ]

        # ------------------------------------------------------------
        # Set up the game board
        # ------------------------------------------------------------
        # Create an empty 6x6 list, of lists
        # Layout in repeating pattern of lists
        # for example if the two given colors are 'R' and 'G'
        # The output board shouls look like this
        # [
        #   [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
        #   [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
        #   [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
        #   [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
        #   [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
        #   [['G'], ['G'], ['R'], ['R'], ['G'], ['G']]
        # ]
        self._gameboard = []
        nextpiece = 0
        for row in range(6):
            thisrow = []
            for colpair in range(3):
                thisrow.append([self._players[nextpiece]["color"]])
                thisrow.append([self._players[nextpiece]["color"]])
                nextpiece = (nextpiece + 1) % 2
            self._gameboard.append(thisrow)

        # ------------------------------------------------------------
        # Set the current turn value
        # ------------------------------------------------------------
        self._current_turn = 0

    def _change_turn(self):
        """
            This method changes the turn to the other player
        """
        self._current_turn = (self._current_turn + 1) % 2

    def _collapse_stack(self, location):
        """
            This method will remove pieces from the
            bottom of that locations stack until there are 5 or less pieces remaining based on location.
            Takes the location as a parameter.

            Also will then add the taken out pieces onto the current players turn's captured or reserved pieces.
        """
        while len(self._gameboard[location[0]][location[1]]) > 5:
            # Remove the piece from the bottom of the stack
            bottom_piece = self._gameboard[location[0]][location[1]].pop(0)
            # Add it to current players reserved or captured
            if (self._players[self._current_turn]["color"] == bottom_piece):
                self._players[self._current_turn]["reserved"] += 1
            else:
                self._players[self._current_turn]["captured"] += 1

    def _isLocationValid(self, location):
        """
            This method will return whether or not it is valid (boolean) based on location as a parameter
        """
        if location[0] < 0 or location[0] > 5:
            return False
        elif location[1] < 0 or location[1] > 5:
            return False
        else:
            return True

    def move_piece(self, player_name, source_location, destination_location, amount_moved):
        """
        This method will take the player name, player's move, coordinate, and location of the move
        as parameters and will then try to check and execute the move.
        If it is a successful move then, the game state will become updated.

        Returns One of:
            False                      : player is trying to make a move out of turn
            False                      : player provides invalid locations
            False                      : player is trying to move invalid number of pieces
            'successfully moved'       : the move was successful
            '<player name> Wins'       : the move caused the player to win
        """
        # Validates that it is this players turn
        if self._players[self._current_turn]["name"] != player_name:
            return False
        # Validate that source location is valid
        # Validate that destination location is valid
        if not self._isLocationValid(source_location) or not self._isLocationValid(destination_location):
            return False
        # Validate move is either horizontal or vertical
        if destination_location[0] != source_location[0] and destination_location[1] != source_location[1]:
            return False
        # Validate that the requested amount of pieces to move are availible in the source stack
        if amount_moved < 1 or amount_moved > len(self._gameboard[source_location[0]][source_location[1]]):
            return False
        # Validate that the piece on top of the source stack belongs to this player
        if self._gameboard[source_location[0]][source_location[1]][-1] != \
                self._players[self._current_turn]["color"]:
            return False
        # Validate that the distance moved is less than or equal to the amount of pieces moved
        if abs(destination_location[0] - source_location[0] + \
               destination_location[1] - source_location[1]) > amount_moved:
            return False
        # Remove requested pieces from current location (preserving stack order)
        # append the moved pieces to the list at the destination location (placing on top of the stack)
        first_index = len(self._gameboard[source_location[0]][source_location[1]]) - amount_moved
        for i in range(amount_moved):
            self._gameboard[destination_location[0]][destination_location[1]].append(
                self._gameboard[source_location[0]][source_location[1]].pop(first_index))
        # call the _collapse_stack method
        self._collapse_stack(destination_location)
        # check if this player just won
        if self._players[self._current_turn]["captured"] >= 6:
            return player_name + ' Wins'
        # call _change_turn
        self._change_turn()
        return "successfully moved"

    def show_pieces(self, position):
        """
        This method will take the position as a parameter and will return a list of the pieces at that specific
        position. The returned list will start with the bottom-most piece, and end with
        the top-most piece.
        """
        return self._gameboard[position[0]][position[1]]

    def show_reserve(self, player_name):
        """
        This method will take the player's name as a parameter and then will return
        the amount of pieces that are in that players reserve.
        """
        for player in self._players:
            if player["name"] == player_name:
                return player["reserved"]
        return 0

    def show_captured(self, player_name):
        """
        This method will take the player's name as a parameter and will
        return the amount of pieces that the player possess.
        """
        for player in self._players:
            if player["name"] == player_name:
                return player["captured"]
        return 0

    def reserved_move(self, player_name, location):
        """
        This method will will take the player's name as a parameter as well as
        a board location. It will then take out one piece from the players reserve and
        will then put it at in that location.

        Will return False if the player does not have pieces in their reserve.
        """
        # validate that it is this players turn
        if self._players[self._current_turn]["name"] != player_name:
            return False
        # validate that destination location is valid
        if not self._isLocationValid(location):
            return False
        # validate that the player has reserve pieces
        if self._players[self._current_turn]["reserved"] == 0:
            return False
        # remove one piece from player reserve
        self._players[self._current_turn]["reserved"] -= 1
        # append piece from player at top of destination stack
        self._gameboard[location[0]][location[1]].append(
            self._players[self._current_turn]["color"])
        # call the _collapse_stack method
        self._collapse_stack(location)
        # check if this player just won
        if self._players[self._current_turn]["captured"] >= 6:
            return player_name + ' Wins'
        # call _change_turn
        self._change_turn()
        return "successfully moved"

# Conditional comments:
# 1. Initializing the board
# Upon the creation of a new FocusGame object. the __init__ function will:
# Create an empty 6x6 list, of lists
# Layout in repeating pattern of lists
# for example if the two given colors are 'R' and 'G'
# The output board shouls look like this
# [
#   [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
#   [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
#   [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
#   [['G'], ['G'], ['R'], ['R'], ['G'], ['G']],
#   [['R'], ['R'], ['G'], ['G'], ['R'], ['R']],
#   [['G'], ['G'], ['R'], ['R'], ['G'], ['G']]
# ]
# 2. Determining how to represent multiple pieces  at a given location on the board
# From the last secenrio, the board is represented as a list of lists, of lists.
# The first two levels of depth represent the locations coordinates
# at self._board[1][2] there is the list that contains the multiple pieces there
# For example to get the bottom piece at location (4,2), internally that will
# be located at self._board[4][2][0]
# 3. Determining how to make singe move, multiple move and reserve move.
# To make a single move or to make a multiple move:
# Call the move_piece method which will:
# validate that it is this players turn
# validate that source location is valid
# validate that destination location is valid
# validate move is either horizontal or vertical
# validate that the piece on top of the source stack belongs to this player
# validate that the requested amount of pieces to move are availible in the source stack
# validate that the distance moved is less than or equal to the amount of pieces moved
# Remove requested pieces from current location (preserving stack order)
# append the moved pieces to the list at the destination location (placing on top of the stack)
# call the _collapse_stack method (explained below* #6)
# check if this player just won
# call _change_turn(explained below* #5)
# To make a reserve move:
# Call reserved_move which will:
# validate that it is this players turn
# validate that destination location is valid
# validate that the player has reserve pieces
# append piece from player at top of destination stack
# remove one piece from player reserve
# call the _collapse_stack method (explained below* #6)
# check if this player just won
# call _change_turn(explained below** #5)
# 4. Remembering captured and reserved pieces for each player.
# both players data will be stored in a list containing two dictionaries
# Both player dicts, should look like the following
# {
#    "name": "PlayerA",
#    "color": "R",
#    "reserved": 0,
#    "captured": 0
# }
# Every time a move is made, pass the destination location to the _collapse_stack(explained below* #6) method to update
# 5. Determining how to track which player's turn is it to play right now.
# The turn is going be stored as the number 0 or 1
# To check if it is a given player_names turn simply:
#   check that player_name == self._players[self._current_turn]["name"]
# When a move is made, call the _change_turn method to:
#   change the current turn to 0, if it was already 1
#   change the current turn to 1, if it was already 0
# 6. Determining how to handle the scenario when a move results in more than 5 pieces at a location.
# Whenever a move is made, the private _collapse_stack method is called:
# given current players turn:
#   for each piece at a given location (until there is only 5 left):
#       remove piece from stack
#       if the pieces color matches the players color
#           add one to players reserve
#       else
#           add one to players captured
