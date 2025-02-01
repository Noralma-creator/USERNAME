{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPmy5YXCmlFgeX1UAw2EC5n",
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
        "<a href=\"https://colab.research.google.com/github/Noralma-creator/USERNAME/blob/master/puzzle.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from logic import *\n",
        "\n",
        "AKnight = Symbol(\"A es un Caballero\")\n",
        "AKnave = Symbol(\"A es un Canalla\")\n",
        "\n",
        "BKnight = Symbol(\"B es un Caballero\")\n",
        "BKnave = Symbol(\"B es un Canalla\")\n",
        "\n",
        "CKnight = Symbol(\"C es un Caballero\")\n",
        "CKnave = Symbol(\"C es un Canalla\")\n",
        "\n",
        "# Puzzle 0\n",
        "# A dice \"Soy un caballero y un canalla.\"\n",
        "conocimiento0 = And(\n",
        "    Or(AKnight, AKnave),  # A es un caballero o un canalla\n",
        "    Not(And(AKnight, AKnave))  # A no puede ser ambos, caballero y canalla\n",
        ")\n",
        "\n",
        "# Puzzle 1\n",
        "# A dice \"Ambos somos canallas.\"\n",
        "# B no dice nada.\n",
        "conocimiento1 = And(\n",
        "    Or(AKnight, AKnave),\n",
        "    Or(BKnight, BKnave),\n",
        "    Not(And(AKnight, AKnave)),\n",
        "    Not(And(BKnight, BKnave)),\n",
        "\n",
        "    # Si A es caballero, entonces lo que dice es cierto (Ambos son canallas, lo cual es falso)\n",
        "    Implication(AKnight, And(AKnave, BKnave)),\n",
        "\n",
        "    # Si A es canalla, su afirmación es falsa (No ambos son canallas, lo que significa que B es caballero)\n",
        "    Implication(AKnave, BKnight)\n",
        ")\n",
        "\n",
        "# Puzzle 2\n",
        "# A dice \"Somos del mismo tipo.\"\n",
        "# B dice \"Somos de tipos diferentes.\"\n",
        "conocimiento2 = And(\n",
        "    Or(AKnight, AKnave),  # A es un caballero o un canalla\n",
        "    Or(BKnight, BKnave),  # B es un caballero o un canalla\n",
        "    Not(And(AKnight, AKnight)),  # A no puede ser ambos # Changed 'Aknight' to 'AKnight'\n",
        "    Not(And(BKnight, BKnave)),  # B no puede ser ambos\n",
        "\n",
        "    # A dice \"Somos del mismo tipo\" → Si A es caballero, esto es cierto; si es canalla, es falso\n",
        "    Implication(AKnight, Biconditional(AKnight, BKnight)),  # Si A es caballero, A y B son iguales\n",
        "    Implication(AKnave, Not(Biconditional(AKnave, BKnave)))  # Si A es canalla, A y B son diferentes\n",
        ")\n",
        "\n",
        "# Puzzle 3\n",
        "# A dice \"Soy un caballero\" o \"Soy un canalla\", pero no se sabe cuál.\n",
        "# B dice \"A dijo 'Soy un canalla'.\"\n",
        "# B también dice \"C es un canalla.\"\n",
        "# C dice \"A es un caballero.\"\n",
        "conocimiento3 = And(\n",
        "    Or(AKnight, AKnave),\n",
        "    Or(BKnight, BKnave),\n",
        "    Or(CKnight, CKnave),\n",
        "    Not(And(AKnight, AKnave)),\n",
        "    Not(And(BKnight, BKnave)),\n",
        "    Not(And(CKnight, CKnave)),\n",
        "\n",
        "    # B dice que \"A dijo 'Soy un canalla'\"\n",
        "    Implication(BKnight, Implication(AKnave, AKnave)),  # Si B es caballero, A realmente dijo \"Soy un canalla\"\n",
        "    Implication(BKnave, Not(Implication(AKnave, AKnave))),  # Si B es canalla, miente sobre lo que dijo A\n",
        "\n",
        "    # B dice que C es un canalla\n",
        "    Implication(BKnight, CKnave),  # Si B es caballero, C realmente es un canalla\n",
        "    Implication(BKnave, CKnight),  # Si B es canalla, miente, y C debe ser caballero\n",
        "\n",
        "    # C dice que A es un caballero\n",
        "    Implication(CKnight, AKnight),  # Si C es caballero, su afirmación es verdadera\n",
        "    Implication(CKnave, AKnave)  # Si C es canalla, su afirmación es falsa\n",
        ")\n",
        "\n",
        "def main():\n",
        "    simbolos = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]\n",
        "    puzzles = [\n",
        "        (\"Puzzle 0\", conocimiento0),\n",
        "        (\"Puzzle 1\", conocimiento1),\n",
        "        (\"Puzzle 2\", conocimiento2),\n",
        "        (\"Puzzle 3\", conocimiento3)\n",
        "    ]\n",
        "\n",
        "    for puzzle, conocimiento in puzzles:\n",
        "        print(puzzle)\n",
        "        if len(conocimiento.conjuncts) == 0:\n",
        "            print(\"    Aún no implementado.\")\n",
        "        else:\n",
        "            for simbolo in simbolos:\n",
        "                if model_check(conocimiento, simbolo):\n",
        "                    print(f\"    {simbolo}\")\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    main()\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "yEZWXRTEveR1",
        "outputId": "31870a6c-7889-4a55-db64-c3b7e4b9faf1"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Puzzle 0\n",
            "Puzzle 1\n",
            "    A es un Canalla\n",
            "    B es un Caballero\n",
            "Puzzle 2\n",
            "    A es un Canalla\n",
            "    B es un Caballero\n",
            "Puzzle 3\n",
            "    A es un Canalla\n",
            "    B es un Caballero\n",
            "    C es un Canalla\n"
          ]
        }
      ]
    }
  ]
}