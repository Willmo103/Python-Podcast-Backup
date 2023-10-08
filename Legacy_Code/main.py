from helper_functions import *

if not get_last_download_dir():
    directory = input("Enter your root download directory\n > ")
    set_dir(directory)

print(f'\n\nCurrent Download Dir: {get_last_download_dir()}')

print("""
    Menu:
    1 -- Enter new RSS urls.
    2 -- List all podcasts presently being downloaded.
    3 -- Download all unsaved podcasts. 
    4 -- Change your root download directory.
    type 'exit' or hit ctrl + 'C' to exit.
""")

option = input('What would you like to do?\n > ')
rss_list = []
add_rss = "None"
while option != "exit":
    if option == "1":
        add_rss = input("\nEnter an RSS url, or hit ENTER to return to menu \n > ")
        while add_rss != "":
            add_new_feed(add_rss)
            create_feed_data(add_rss)
            print(f"'{get_title(add_rss)}' was added to your download queue.")
            add_rss = input("\nEnter an RSS url, or hit ENTER to return to menu \n > ")

    elif option == "2":
        display_podcast_names()

    elif option == "3":
        feeds = load_feeds()
        for feed in feeds:
            check_for_new(feeds[feed])
        ready = input("\nPress enter to begin download.")
        if not ready:
            print("\nDownloading...")
            download_all()

    elif option == "4":
        directory = input("Enter your root download directory\n > ")
        set_dir(directory)

    print("""
    Menu:
    1 -- Enter new RSS urls.
    2 -- List all podcasts presently being downloaded.
    3 -- Download all unsaved podcasts. 
    4 -- Change your root download directory.
    type 'exit' or hit ctrl + 'C' to exit.
    """)

    option = input('What would you like to do?\n > ')
