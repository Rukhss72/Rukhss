import random
import csv
import tkinter as tk
from tkinter import simpledialog

mauritian_slots = [
    {"name": "Go", "group": "      Special", "color": "palegreen1", "price": "Rs 0"},
    {"name": "Flacq", "group": "      Group 1", "color": "brown", "price": "Rs 0"},
    {"name": "Cpe1", "group": "      Group 1", "color": "brown", "price": "Rs 60"},
    {"name": "    C.Chest1", "group": "      Special", "color": "hotpink", "price": "Rs 0"},
    {"name": "MBG1", "group": "      Railroad", "color": "springgreen4", "price": "Rs 200"},
    {"name": "Flac1", "group": "      Group 1", "color": "brown", "price": "Rs 60"},
    {"name": "Tax", "group": "      Special", "color": "blueviolet", "price": "Rs 0"},
    {"name": " G.Baie", "group": "      Group 2", "color": "light blue", "price": "Rs 100"},
    {"name": "   Chance1", "group": "      Special", "color": "steelblue", "price": "Rs 0"},
    {"name": "   R.Hill1", "group": "      Group 2", "color": "light blue", "price": "Rs 100"},
    {"name": "      Q.Bornes", "group": "      Group 2", "color": "light blue", "price": "Rs 120"},
    {"name": "Visit", "group": "      Special", "color": "palegreen3", "price": "Rs 0"},
    {"name": "P.L1", "group": "      Group 3", "color": "pink", "price": "Rs 140"},
    {"name": "      Electricity", "group": "      Utility", "color": "gold", "price": "Rs 150"},
    {"name": "      B.Bassin1", "group": "      Railroad", "color": "springgreen4", "price": "Rs 140"},
    {"name": "    Vacoas", "group": "       Group 3", "color": "pink", "price": "Rs 160"},
    {"name": " Moka", "group": "     Group 3", "color": "pink", "price": "Rs 200"},
    {"name": " Tayack", "group": "      Group 4", "color": "orange", "price": "Rs 180"},
    {"name": "    C.Chest2", "group": "      Special", "color": "hotpink", "price": "Rs 0"},
    {"name": "    R.Belle", "group": "      Group 4", "color": "orange", "price": "Rs 180"},
    {"name": "Mbg", "group": "      Group 4", "color": "orange", "price": "Rs 200"},
    {"name": "Park", "group": "      Special", "color": "blueviolet", "price": "Rs 0"},
    {"name": "B.Air", "group": "      Group 5", "color": "red", "price": "Rs 220"},
    {"name": "   Chance2", "group": "      Special", "color": "steelblue", "price": "Rs 0"},
    {"name": "  G.Port", "group": "      Group 5", "color": "red", "price": "Rs 220"},
    {"name": " Metro", "group": "      Railroad", "color": "springgreen4", "price": "Rs 200"},
    {"name": " R.Hill2", "group": "      Group 5", "color": "red", "price": "Rs 240"},
    {"name": " B.River", "group": "      Group 6", "color": "yellow", "price": "Rs 260"},
    {"name": "    Rempart", "group": "      Group 6", "color": "yellow", "price": "Rs 260"},
    {"name": " Water", "group": "   Utility", "color": "gold", "price": "Rs 150"},
    {"name": " Albion", "group": "      Group 6", "color": "yellow", "price": "Rs 280"},
    {"name": "Cpe2", "group": "     Group 7", "color": "green", "price": "Rs 300"},
    {"name": "RDA2", "group": "      Group 7", "color": "green", "price": "Rs 300"},
    {"name": "    C.Chest3", "group": "      Special", "color": "hotpink", "price": "Rs 0"},
    {"name": "P.L2", "group": "      Group 7", "color": "green", "price": "Rs 320"},
    {"name": "RDA2", "group": "      Railroad", "color": "springgreen4", "price": "Rs 200"},
    {"name": "    Chance3", "group": "      Special", "color": "steelblue", "price": "Rs 0"},
    {"name": "Pl3", "group": "      Group 8", "color": "blue", "price": "Rs 350"},
    {"name": "Tax", "group": "      Special", "color": "blueviolet", "price": "Rs 0"},
    {"name": "Flac2", "group": "      Group 8", "color": "blue", "price": "Rs 400"},
    {"name": "Flac3", "group": "      Group 8", "color": "blue", "price": "Rs 400"},
    {"name": "Flac4", "group": "      Group 8", "color": "blue", "price": "Rs 400"},
]
class MonopolyGame:
    def __init__(self, root, players, board):
        self.root = root  # The Tkinter root window.
        self.players = players  # List of players.
        self.board = board  # The game board.
        self.current_player_index = 0  # Index to track the current player.
        self.board_size = len(board)  # Total number of slots on the board.
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Monopoly Game")

        # Create a button to roll the dice and link it to the roll_dice method.
        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=10)


        self.dice_label = tk.Label(self.root, text="Dice Roll: ", font=("Helvetica", 12))
        self.dice_label.pack()

        self.dice_value = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.dice_value.pack()

        # Create a canvas to draw the game board.
        self.board_canvas = tk.Canvas(self.root, width=600, height=600) # w..16cm & h..16cm in pixel
        self.board_canvas.pack()

        self.draw_board()  # Draw the initial board.

    def roll_dice(self):
        dice_value = random.randint(1, 6)  # Generate a random dice value between 1 and 6.
        self.dice_value.config(text=str(dice_value))  # Update the dice value label.
        player = self.players[self.current_player_index]  # Get the current player.
        if player["player_num"] % 2 == 0:  # Check if the player number is even.
            self.move_player_clockwise(dice_value)
        else:
            self.move_player_anti_clockwise(dice_value)

    def move_player_clockwise(self, dice_value):
        player = self.players[self.current_player_index]  # Get the current player.
        player["position"] = (player["position"] + dice_value) % self.board_size  # Update the player's position clockwise.
        self.log_movement(player)  # Log the player's movement.
        self.current_player_index = (self.current_player_index + 1) % len(self.players)  # Move to the next player.
        self.draw_board()  # Redraw the board to update player positions.

    def move_player_anti_clockwise(self, dice_value):
        player = self.players[self.current_player_index]  # Get the current player.
        player["position"] = (player["position"] - dice_value) % self.board_size  # Update the player's position anti-clockwise.
        self.log_movement(player)  # Log the player's movement.
        self.current_player_index = (self.current_player_index + 1) % len(self.players)  # Move to the next player.
        self.draw_board()  # Redraw the board to update player positions.

    def log_movement(self, player):
        slot = self.board[player["position"]]  # Get the slot where the player landed.

        with open('player_movements.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [player["name"], player["player_num"], player["position"], slot["name"], slot["group"], slot["color"],slot["price"]])

    def draw_board(self):
        self.board_canvas.delete("all")
        self.board_canvas.config(bg="darkseagreen1")  # Set the background color of the canvas
        slot_size = 55  # Define the size of each slot on the board.
        board_size = 11  # Define the size of the board grid (11x11).

        # Loop through each slot and draw it on the canvas.
        for i, slot in enumerate(self.board):
            if i < 10:
                # Bottom row
                Row_1, Column_1 = (9 - i) * slot_size, 10 * slot_size
            elif i < 20:
                # Left column
                Row_1, Column_1 = 0, (19 - i) * slot_size
            elif i < 30:
                # Top row
                Row_1, Column_1 = (i - 20) * slot_size, 0
            elif i < 41:
                # Right column
                Row_1, Column_1 = 10 * slot_size, (i - 30) * slot_size

            Row_2, Column_2 = Row_1 + slot_size, Column_1 + slot_size  # Define the opposite corner of the slot.
            color = slot["color"]  # Get the slot color.
            # Draw the slot rectangle on the canvas.
            self.board_canvas.create_rectangle(Row_1, Column_1, Row_2, Column_2, fill=color, outline="black")
            # Draw the slot name text.
            self.board_canvas.create_text(Row_1 + slot_size / 3, Column_1 + slot_size / 3 - 10, text=slot["name"],
                                          fill="black")
            # Draw the slot price text.
            self.board_canvas.create_text(Row_1 + slot_size / 2, Column_1 + slot_size / 2 + 10, text=slot["price"],
                                          fill="black")
            # Draw the slot group text
            self.board_canvas.create_text(Row_1 + slot_size / 4, Column_1 + slot_size / 4 + 10, text=slot["group"],
                                          fill="black")

        # Loop through each player and draw their position on the board.
        player_colors = ["darkred", "black", "navy", "violet", "gray", "purple", "teal", "aqua"]  # Define a list of player colors
        for i, player in enumerate(self.players):
            pos = player["position"]  # Get the player's position.
            if pos < 10:
                # Bottom row
                Row_1, Column_1 = (9 - pos) * slot_size, 10 * slot_size
            elif pos < 20:
                # Left column
                Row_1, Column_1 = 0, (19 - pos) * slot_size
            elif pos < 30:
                # Top row
                Row_1, Column_1 = (pos - 20) * slot_size, 0
            elif pos < 41:
                # Right column
                Row_1, Column_1 = 10 * slot_size, (pos - 30) * slot_size

            # Draw the player's position as a colored circle on the board. (token)
            player_color = player_colors[i % len(player_colors)]  # Assign a color to each player
            self.board_canvas.create_oval(Row_1 + 10, Column_1 + 10, Row_1 + 30, Column_1 + 30, fill=player_color)

def main():
    root = tk.Tk()
    board = mauritian_slots
    players = []

    num_players = simpledialog.askinteger("Input", "Enter number of players (2-8):", minvalue=2, maxvalue=8)

    # Loop through the number of players and get their names.
    for i in range(num_players):
        name = simpledialog.askstring("Input", f"Enter name for Player {i + 1}:")
        players.append({"name": name, "player_num": i + 1, "position": 0})

    game = MonopolyGame(root, players, board)
    root.mainloop()

if __name__ == "__main__":
    main()