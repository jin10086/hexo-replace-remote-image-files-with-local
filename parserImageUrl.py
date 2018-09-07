import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension

# ref:https://stackoverflow.com/questions/29259912/how-can-i-get-a-list-of-image-urls-from-a-markdown-file-in-python
# First create the treeprocessor


class ImgExtractor(Treeprocessor):
    def run(self, doc):
        "Find all images and append to markdown.images. "
        self.markdown.images = []
        for image in doc.findall(".//img"):
            self.markdown.images.append(image.get("src"))


# Then tell markdown about it


class ImgExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        img_ext = ImgExtractor(md)
        md.treeprocessors.add("imgext", img_ext, ">inline")


# Finally create an instance of the Markdown class with the new extension


def parser(data):
    ""
    md = markdown.Markdown(extensions=[ImgExtExtension()])
    html = md.convert(data)
    return md.images


def testParse():
    data = """
        **this is some markdown**
        blah blah blah
        ![image here](http://somewebsite.com/image1.jpg)
        ![another image here](http://anotherwebsite.com/image2.jpg)
    """
    assert parser(data) == [
        "http://somewebsite.com/image1.jpg",
        "http://anotherwebsite.com/image2.jpg",
    ]
