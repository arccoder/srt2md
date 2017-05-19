"""
Merge .srt files from udacity videos into single .md file.
http://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
"""
import os
import re


def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from http://stackoverflow.com/a/12643073/190597
    '''
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]


def listFilesInFolderWithExt(in_folder, extension=""):
    """
    List files with extension in in_folder

    Args:
        in_folder (str): Path to the input folder
        extension (str): extension of files to list

    Returns:
        (list): list of the files in the in_folder with extension
    """
    assert in_folder is not None, "Input error: in_folder not available"
    assert extension is not None, "Input error: extension not available"

    file_list = []
    for root, dirs, files in os.walk(in_folder):
        for file in files:
            if file.endswith(extension):
                file_list.append(in_folder + file)

    return file_list


def mergeMdFiles(in_folder, out_file_name):
    """
    Merge .md files  within in_folder into one .md file.

    Args:
        in_folder (str): Path to the input folder
        out_file_name (str): Output file name

    Returns:

    """
    assert in_folder is not None, "Input error: in_folder not available"
    assert out_file_name is not None, "Input error: out_file_name not available"

    file_list = listFilesInFolderWithExt(in_folder, "md")

    with open(out_file_name, "wb") as outfile:
        for f in file_list:
            with open(f, "rb") as infile:
                outfile.write("## " + f[len(in_folder):-3] + "\n\n")
                outfile.write(infile.read())
                outfile.write("\n\n")

    return


def srtInFolder2Md(in_folder, files):
    """
    Merge .srt files into one md within the in_folder

    Args:
        in_folder (str): Path to the folder with srt files
        files (list): List of files in the in_folder

    Returns:
        (str): Contents in the files merged into string
    """
    assert in_folder is not None, "Input error: in_folder not available"
    assert files is not None, "Input error: files not available"

    finalString = ""

    for filename in files:
        finalString += "### " + filename[:-4] + "\n\n"

        with open(in_folder + "/" + filename) as infile:
            lines = infile.readlines()

        for line in lines:
            line = line[:-1]
            if len(line) < 3 or (":" in line and "-->" in line):
                continue

            if line.endswith(".") or line.endswith("?"):
                finalString += line + "\n\n"
            else:
                finalString += line + " "

    return finalString


def srtInFolders2Md(root_folder, out_file_name):
    """
    Call srtInFolder2Md on the folders within the root_folder

    Args:
        root_folder (str): Path that contains folders with srt files in them
        out_file_name (str): Path to the out_file_name to save .md files

    Returns:

    """
    assert root_folder is not None, "Input argument root_folder is null"
    assert out_file_name is not None, "Input argument out_file_name is null"

    if not os.path.exists(root_folder):
        print("%s does not exist" % root_folder)
        return

    directories = os.walk(root_folder).next()[1]
    directories.sort(key=natural_keys)

    finalString = ""
    for directory in directories:
        for _, _, files in os.walk(root_folder + "/" + directory):
            if len(files) > 0:
                finalString += "## " + directory + "\n\n" + \
                               srtInFolder2Md(root_folder + "/" + directory, files) + "\n\n\n"

    with open(out_file_name, "w") as outfile:
        outfile.write("%s" % finalString)

    return
