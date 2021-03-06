from QuoteMaker import QuoteMaker
from PIL import Image

def main():
    quote_maker = QuoteMaker()

    avatar_img = Image.open('./img/marilyn.jpg')
    nickname = 'Lorem Ipsum'
    message = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
        "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
        "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
   
    quote = quote_maker.create_quote(avatar_img, message, nickname)
    quote.save('./img/quote.png')

if __name__ == "__main__":
    main()