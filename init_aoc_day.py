import os
import shutil
import requests
import nbformat as nbf
from dotenv import load_dotenv
from bs4 import BeautifulSoup


def scrape_samples(year, day, session_token, folder_name):
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {"session": session_token}
    response = requests.get(url, cookies=cookies)
    if response.status_code != 200:
        print(f"Failed to fetch puzzle page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    code_blocks = soup.find_all("pre")

    for i, block in enumerate(code_blocks):
        code = block.get_text().strip()
        filename = f"sample{'' if i == 0 else i+1}.txt"
        path = os.path.join(folder_name, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Saved sample to: {filename}")


def get_day_input(year, day, session_token):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session_token}
    response = requests.get(url, cookies=cookies)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch input: {response.status_code}")
    return response.text


def create_notebook(path, day, year):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            f"# 🎄 Advent of Code {year} - Day {day:02d}\nhttps://adventofcode.com/{year}/day/{day}"
        ),
        nbf.v4.new_code_cell(
            "import numpy as np\n"
            "import re\n"
            "import json\n"
            "import math\n\n"
            "# Load input\n"
            "with open('sample.txt') as f:\n"
            "    data = f.read().strip()\n"
            "    print(data)\n"
        ),
        nbf.v4.new_markdown_cell("## ⭐ Part 1"),
        nbf.v4.new_code_cell(
            "# Part 1 solution\n"
            "def part1(data):\n"
            "    pass  # TODO: implement\n"
            "\n"
            "# print(part1(data))"
        ),
        nbf.v4.new_markdown_cell("## ⭐ Part 2"),
        nbf.v4.new_code_cell(
            "# Part 2 solution\n"
            "def part2(data):\n"
            "    pass  # TODO: implement\n"
            "\n"
            "# print(part2(data))"
        ),
    ]
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Created notebook: {path}")


def create_day_folder(day, year, session_token):
    folder_name = f"day{day:02d}"

    if os.path.exists(folder_name):
        choice = input(
            f"Folder '{folder_name}' already exists. Delete and recreate? (y/n): "
        ).lower()
        if choice == "y":
            shutil.rmtree(folder_name)
        else:
            print("Aborted.")
            return

    os.makedirs(folder_name)
    print(f"Created folder: {folder_name}")

    # Create Jupyter notebook
    notebook_path = os.path.join(folder_name, f"{folder_name}.ipynb")
    create_notebook(notebook_path, day, year)

    # Fetch input
    try:
        input_data = get_day_input(year, day, session_token)
        input_file = os.path.join(folder_name, "input.txt")
        with open(input_file, "w") as f:
            f.write(input_data.strip())
        print(f"Fetched input and saved to: {input_file}")

        # Scrape and save samples
        scrape_samples(year, day, session_token, folder_name)
    except Exception as e:
        print(e)


def main():
    load_dotenv()
    session_token = os.getenv("AOC_SESSION")
    year = 2025  # You can make this dynamic if you want
    day = int(input("Which day would you like to initialize? (1-25): "))
    create_day_folder(day, year, session_token)


if __name__ == "__main__":
    main()
