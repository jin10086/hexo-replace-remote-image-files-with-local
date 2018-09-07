from parserImageUrl import parser
from downloadImage import download
import re
import pathlib
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


findImagePatten = re.compile(r"!\[(.*?)\)")
findImageTextPatten = re.compile("!\[(.*?)\]")
findImageUrlPatten = re.compile("\((.*?)\)")
findImageTagPatten = re.compile("!.*?\)")


def replace(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, "w") as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)


def main(basedir):
    for fname in pathlib.Path(basedir).glob("*.md"):
        with open(fname, "r+") as f:
            count = 0
            for i in f.readlines():
                if findImagePatten.findall(i):
                    text = findImageTextPatten.findall(i)[0]
                    imageUrl = findImageUrlPatten.findall(i)[0]
                    imageType = imageUrl.split(".")[-1]
                    if len(imageType) >= 4:  # fix images url don't have suffix
                        imageType = "jpg"
                    imageFilename = fname.parent.joinpath(
                        fname.name.split(".md")[0]
                    ) / "{}.{}".format(str(count), imageType)
                    count += 1
                    old = findImageTagPatten.findall(i)[0]
                    new = "{% asset_img " + imageFilename.name + " " + text + " %}"
                    replace(fname, old, new)

                    x = pathlib.Path(imageFilename)
                    if not x.parent.exists():
                        x.parent.mkdir(parents=True)
                    download(imageUrl, imageFilename)


if __name__ == "__main__":
    basedir = "/Users/gaojin/Documents/GitHub/jin10086.github.io/source/_posts"
    main(basedir)
