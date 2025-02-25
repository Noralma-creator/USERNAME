{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMYruVlrGauQyaYq/rzuhUJ",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Noralma-creator/USERNAME/blob/master/minesweeper.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Y1dMhsbOkvcQ",
        "outputId": "ece4a65a-d73c-4544-a617-a029957364dd"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Tablero inicial:\n",
            "-----------------\n",
            "| | | |X| | |X| |\n",
            "-----------------\n",
            "| | | | | | | | |\n",
            "-----------------\n",
            "| | |X| |X| | | |\n",
            "-----------------\n",
            "| | | | | | | |X|\n",
            "-----------------\n",
            "| | | | | | | | |\n",
            "-----------------\n",
            "| | | | |X| | | |\n",
            "-----------------\n",
            "| | | | | | | | |\n",
            "-----------------\n",
            "| | | | | |X| |X|\n",
            "-----------------\n"
          ]
        }
      ],
      "source": [
        "import itertools\n",
        "import random\n",
        "\n",
        "\n",
        "class Minesweeper:\n",
        "    \"\"\"\n",
        "    Minesweeper game representation\n",
        "    \"\"\"\n",
        "\n",
        "    def __init__(self, height=8, width=8, mines=8):\n",
        "\n",
        "        # Set initial width, height, and number of mines\n",
        "        self.height = height\n",
        "        self.width = width\n",
        "        self.mines = set()\n",
        "\n",
        "        # Initialize an empty field with no mines\n",
        "        self.board = [[False for _ in range(self.width)] for _ in range(self.height)]\n",
        "\n",
        "        # Add mines randomly\n",
        "        while len(self.mines) != mines:\n",
        "            i = random.randrange(height)\n",
        "            j = random.randrange(width)\n",
        "            if not self.board[i][j]:\n",
        "                self.mines.add((i, j))\n",
        "                self.board[i][j] = True\n",
        "\n",
        "        # At first, player has found no mines\n",
        "        self.mines_found = set()\n",
        "\n",
        "    def print(self):\n",
        "        \"\"\"\n",
        "        Prints a text-based representation\n",
        "        of where mines are located.\n",
        "        \"\"\"\n",
        "        for i in range(self.height):\n",
        "            print(\"--\" * self.width + \"-\")\n",
        "            for j in range(self.width):\n",
        "                if self.board[i][j]:\n",
        "                    print(\"|X\", end=\"\")\n",
        "                else:\n",
        "                    print(\"| \", end=\"\")\n",
        "            print(\"|\")\n",
        "        print(\"--\" * self.width + \"-\")\n",
        "\n",
        "    def is_mine(self, cell):\n",
        "        i, j = cell\n",
        "        return self.board[i][j]\n",
        "\n",
        "    def nearby_mines(self, cell):\n",
        "        \"\"\"\n",
        "        Returns the number of mines that are\n",
        "        within one row and column of a given cell,\n",
        "        not including the cell itself.\n",
        "        \"\"\"\n",
        "\n",
        "        count = 0\n",
        "        for i in range(cell[0] - 1, cell[0] + 2):\n",
        "            for j in range(cell[1] - 1, cell[1] + 2):\n",
        "                if (i, j) == cell:\n",
        "                    continue\n",
        "                if 0 <= i < self.height and 0 <= j < self.width and self.board[i][j]:\n",
        "                    count += 1\n",
        "\n",
        "        return count\n",
        "\n",
        "    def won(self):\n",
        "        \"\"\"\n",
        "        Checks if all mines have been flagged.\n",
        "        \"\"\"\n",
        "        return self.mines_found == self.mines\n",
        "\n",
        "\n",
        "class Sentence:\n",
        "    \"\"\"\n",
        "    Logical statement about a Minesweeper game\n",
        "    A sentence consists of a set of board cells,\n",
        "    and a count of the number of those cells which are mines.\n",
        "    \"\"\"\n",
        "\n",
        "    def __init__(self, cells, count):\n",
        "        self.cells = set(cells)\n",
        "        self.count = count\n",
        "\n",
        "    def __eq__(self, other):\n",
        "        return self.cells == other.cells and self.count == other.count\n",
        "\n",
        "    def __str__(self):\n",
        "        return f\"{self.cells} = {self.count}\"\n",
        "\n",
        "    def known_mines(self):\n",
        "        \"\"\"\n",
        "        Returns the set of all cells in self.cells known to be mines.\n",
        "        \"\"\"\n",
        "        if len(self.cells) == self.count:\n",
        "            return self.cells\n",
        "        return set()\n",
        "\n",
        "    def known_safes(self):\n",
        "        \"\"\"\n",
        "        Returns the set of all cells in self.cells known to be safe.\n",
        "        \"\"\"\n",
        "        if self.count == 0:\n",
        "            return self.cells\n",
        "        return set()\n",
        "\n",
        "\n",
        "    def mark_mine(self, cell):\n",
        "        \"\"\"\n",
        "        Updates internal knowledge representation given the fact that\n",
        "        a cell is known to be a mine.\n",
        "        \"\"\"\n",
        "\n",
        "        if cell in self.cells:\n",
        "            self.cells.remove(cell)\n",
        "            self.count -= 1\n",
        "\n",
        "\n",
        "    def mark_safe(self, cell):\n",
        "        \"\"\"\n",
        "        Updates internal knowledge representation given the fact that\n",
        "        a cell is known to be safe.\n",
        "        \"\"\"\n",
        "        if cell in self.cells:\n",
        "            self.cells.remove(cell)\n",
        "\n",
        "\n",
        "class MinesweeperAI:\n",
        "    def __init__(self, height=8, width=8):\n",
        "        self.height = height\n",
        "        self.width = width\n",
        "        self.moves_made = set()\n",
        "        self.mines = set()\n",
        "        self.safes = set()\n",
        "        self.knowledge = []\n",
        "\n",
        "    def mark_mine(self, cell):\n",
        "        self.mines.add(cell)\n",
        "        for sentence in self.knowledge:\n",
        "            sentence.mark_mine(cell)\n",
        "\n",
        "    def mark_safe(self, cell):\n",
        "        self.safes.add(cell)\n",
        "        for sentence in self.knowledge:\n",
        "            sentence.mark_safe(cell)\n",
        "\n",
        "    def add_knowledge(self, cell, count):\n",
        "        self.moves_made.add(cell)\n",
        "        self.mark_safe(cell)\n",
        "        neighbors = set()\n",
        "        for i in range(cell[0] - 1, cell[0] + 2):\n",
        "            for j in range(cell[1] - 1, cell[1] + 2):\n",
        "                if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:\n",
        "                    if (i, j) not in self.safes and (i, j) not in self.mines:\n",
        "                        neighbors.add((i, j))\n",
        "\n",
        "        self.knowledge.append(Sentence(neighbors, count))\n",
        "\n",
        "        for sentence in self.knowledge:\n",
        "            for mine in sentence.known_mines():\n",
        "                self.mark_mine(mine)\n",
        "            for safe in sentence.known_safes():\n",
        "                self.mark_safe(safe)\n",
        "\n",
        "        self.knowledge = [s for s in self.knowledge if s.cells]\n",
        "\n",
        "    def make_safe_move(self):\n",
        "        for cell in self.safes:\n",
        "            if cell not in self.moves_made:\n",
        "                return cell\n",
        "        return None\n",
        "\n",
        "    def make_random_move(self):\n",
        "        possible_moves = [\n",
        "            (i, j)\n",
        "            for i in range(self.height)\n",
        "            for j in range(self.width)\n",
        "            if (i, j) not in self.moves_made and (i, j) not in self.mines]\n",
        "\n",
        "        return random.choice(possible_moves) if possible_moves else None\n",
        "\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    try:\n",
        "        # Crear una instancia del juego\n",
        "        game = Minesweeper()\n",
        "\n",
        "        # Imprimir el tablero inicial\n",
        "        print(\"Tablero inicial:\")\n",
        "        game.print()\n",
        "\n",
        "        # Puedes agregar más lógica aquí para interactuar con el juego.\n",
        "\n",
        "    except Exception as e:\n",
        "        print(f\"Ha ocurrido un error: {e}\")\n",
        "    finally:\n",
        "        input(\"Presiona Enter para salir...\")"
      ]
    }
  ]
}