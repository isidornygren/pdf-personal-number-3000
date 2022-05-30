import re, os, pdftotext, argparse, glob

regex = re.compile(r"personnummer\s*(\d{6}(\d{2})?-\d{4})")

parser = argparse.ArgumentParser(description="PDF Personal number renamer 3000")

parser.add_argument(
    "paths",
    type=str,
    help="Whitespace separated globable path(s) that should be searched",
    nargs="+",
)

parser.add_argument(
    "-n",
    "--no_safety",
    action="store_const",
    const=True,
    help="Disable yes/no question when renaming files (use with extreme caution)",
)

args = parser.parse_args()

for glob_path in args.paths:
    paths = glob.glob(glob_path)
    if len(paths) == 0:
        print('No files matching the glob "{0}" found.'.format(glob_path))

    for path in paths:
        print('File "{0}" found.'.format(path))

        with open(path, "rb") as f:
            pdf = pdftotext.PDF(f)

        for page in pdf:
            matches = list(re.finditer(regex, page))
            match = None
            if len(matches) == 1:
                match = matches[0]
            if len(matches) > 1:
                print(
                    "Multiple matches found, choose a match to use (0-{0}):".format(
                        len(matches) - 1
                    )
                )
                for index, m in enumerate(matches):
                    print("\t[{0}]: {1}".format(index, m.group(1)))
                match = matches[int(input())]

            if match:
                if not args.no_safety:
                    # The second group match should be the personal number
                    print("Personal number match found:", match.group(1))
                    new_name = match.group(1) + ".pdf"
                    should_rename = input(
                        'Would you like to rename "{0}" to "{1}"? (y/n): '.format(
                            path, new_name
                        )
                    )
                    if should_rename in ["yes", "Yes", "y", "Y"]:
                        os.rename(path, match.group(1) + ".pdf")
                else:
                    os.rename(path, match.group(1) + ".pdf")
