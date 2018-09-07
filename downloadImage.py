import requests


def download(url, imageName):
    with open(imageName, "wb") as f:
        z = requests.get(
            url,
            headers={
                "user-agent": "Mozilla/5.0 (MacintoshIntel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
            },
        )
        f.write(z.content)


def main():
    download(
        "https://raw.githubusercontent.com/crew102/reprexpy/master/docs/source/gifs/basic-example.gif",
        r"wtf/123/hello/123",
    )


if __name__ == "__main__":
    main()
