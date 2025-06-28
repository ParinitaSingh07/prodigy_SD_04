import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        # Title label
        title = tk.Label(root, text="Sudoku Solver", font=('Arial', 24, 'bold'))
        title.grid(row=0, column=0, columnspan=9, pady=10)

        # Instruction label
        instruction = tk.Label(root, text="Enter the numbers that are in the grid", font=('Arial', 12))
        instruction.grid(row=1, column=0, columnspan=9, pady=5)

        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        grid_frame = tk.Frame(self.root)
        grid_frame.grid(row=2, column=0, columnspan=9)

        for row in range(9):
            for col in range(9):
                entry = tk.Entry(grid_frame, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=row, column=col, padx=(3 if col % 3 == 0 else 1, 3 if col % 3 == 3 else 1),
                           pady=(2 if row % 3 == 0 else 1, 2 if row % 3 == 2 else 1))
                
                entry.bind("<KeyRelease>", self.make_bold_on_input)
                self.entries[row][col] = entry

                
    def make_bold_on_input(self, event):
        widget = event.widget
        value = widget.get()
        if value.strip() == '':
            widget.config(font=('Arial', 18, 'normal'))
        else:
            widget.config(font=('Arial', 18, 'bold'), fg='black')

    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve, font=('Arial', 14), bg='lightblue')
        solve_button.grid(row=3, column=0, columnspan=9, sticky="we", pady=10)

    def get_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.entries[row][col].get()
                if val == '':
                    current_row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            current_row.append(num)
                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Invalid number at row {row+1}, column {col+1}")
                        return None
            board.append(current_row)
        return board

    def update_board(self, board):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(board[row][col]))

    def solve(self):
        board = self.get_board()
        if board is None:
            return

        if self.backtrack(board):
            self.update_board(board)
        else:
            messagebox.showinfo("No Solution", "No solution exists for the given Sudoku puzzle.")

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def backtrack(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.backtrack(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()

