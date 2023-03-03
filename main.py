"""
main.py
reads in data files to NLP library and creates visualizations

"""

from nlp_library import Text, map_parts_speech
import pprint as pp
import os
import regex as re


def read_file(filename):
    """

    :param filename: string
        name of file
    :return: data: dictionary
        contains keys as years and values as political affiliation
    """
    data = {}
    with open(filename, "r") as infile:
        file_data = infile.readlines()
        for line in file_data[1:]:
            line = line.strip().split("\t")
            data[int(line[0])] = line[-1]
    return data


def read_directory_files(directory):
    """

    :param directory: string
        path directory to folder that contains all files
    :return: paths: list
        contains path directory for each file
    """
    # iterate over files in that directory
    paths = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            paths.append(f)
    return paths


def main():
    # creates dictionary with president political affiliations by year
    party_by_year = read_file("president_affiliation.txt")

    # reads in all text files with SOTU speeches
    paths = read_directory_files("sotu")
    tt = Text()
    for path in paths:
        tt.load_text(
            path,
            year=int(re.findall('\d+', path)[0]),
            label=party_by_year[int(re.findall('\d+', path)[0])],
            title=path.split(".")[0].replace("_", " ").replace("sotu/", "")
        )

    # cleans data
    tt.frequency_filter(10, "word count")
    tt.frequency_filter(10, "parts of speech")
    tt.rename_keys("parts of speech",
                   map_parts_speech("Parts_of_Speech.txt")
    )

    # creates word cloud with 20-year periods
    tt.time_word_cloud(20, 1939, 2020, ["Republican", "Democrat"])

    # creates word cloud with 10-year periods
    tt.time_word_cloud(10, 1939, 2020, ["Republican", "Democrat"])

    # creates sankey diagram
    tt.sankey_diagram(min_common_words=500,
                      label_color_dict={'Republican': (255, 0, 0),
                                        'Democrat': (0, 0, 255)
                      },
                      min_year=1936
    )

    # creates line plot of readability difficulty over time
    color_map = {"Democrat": "blue",
                 "Republican": "red"
    }
    tt.plot_over_time("readability difficulty",
                      split_year=1936,
                      color_map=color_map
    )


if __name__ == '__main__':
    main() 
