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

print(args.no_safety)

for glob_path in args.paths:
    paths = glob.glob(glob_path)
    if len(paths) == 0:
        print('No files matching the glob "' + glob_path + '" found.')

    for path in paths:
        print('File "' + path + '" found.')

        with open(path, "rb") as f:
            pdf = pdftotext.PDF(f)

        for page in pdf:
            match = re.search(regex, page)
            if match:
                # The second group match should be the personal number
                if not args.no_safety:
                    print('Personal number match found: "' + match.group(1) + '"')
                    new_name = match.group(1) + ".pdf"
                    should_rename = input(
                        'Would you like to rename "'
                        + path
                        + '" to "'
                        + new_name
                        + '"? (y/n): '
                    )
                    if should_rename in ["yes", "Yes", "y", "Y"]:
                        os.rename(path, match.group(1) + ".pdf")
                else:
                    os.rename(path, match.group(1) + ".pdf")
