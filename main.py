import argparse
import pypub
import utils
import pandas as pd

import variables

# Initialize parser
parser = argparse.ArgumentParser(description="Tool to download book as epub")
parser.add_argument("-i", "--Id", help="Ebook identifier")
parser.add_argument("-u", "--Username", help="User name (email)")
parser.add_argument("-p", "--Password", help="User password (email)")
args = parser.parse_args()

try:
    if args.Id is None:
        raise RuntimeError("Missing book argument!")
    if args.Username is None:
        raise RuntimeError("Missing username argument!")
    if args.Password is None:
        raise RuntimeError("Missing password argument!")

    variables.epub_id = args.Id
    variables.user_name = args.Username
    variables.user_password = args.Password

    # init http session
    utils.init_http_session()


    # get epub definition data
    data = utils.get_epub_definition_json()
    title = data['title']
    spine_url = data['spine']
    spine_json = utils.get_epub_json(spine_url)
    spine_df = pd.DataFrame(spine_json['results'])
    files_url = data['files']
    files_json = utils.get_epub_json(files_url)
    files_df = pd.DataFrame(files_json['results'])


    # init epub
    epub = pypub.Epub(title)
    print("Init epub", title)


    # add chapters
    for index, row in spine_df.iterrows():
        chapter_title = row['title']
        print("Add chapter", chapter_title)
        chapter_url = files_df['url'][index]
        c = pypub.create_chapter_from_url(chapter_url, chapter_title)
        epub.add_chapter(c)


    # generate epub
    print("Generate epub", title)
    epub.create_epub("dist")

except RuntimeError as e:
    print(e)