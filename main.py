import yadisk
from dotenv import load_dotenv
import os

load_dotenv()

this_dir = '/Книги/Квант/2011'
path_to = ''
TOKEN = os.getenv("TOKEN")

client = yadisk.Client(token=f"{TOKEN}")


def look_dir(path: str="") -> list:
    with client:
        return [book.name for book in list(client.listdir(f'{path}'))]

def change_dir(path: str=''):
    global this_dir
    with client:
        if path == '..':
            this_dir = '/'.join(this_dir.split('/')[:-1]) 
        elif path[0] == '/':
            this_dir = path
        else: 
            if client.exists(this_dir + '/' + path): 
                this_dir = this_dir + '/' + path     

def mk_dir(path: str='', name: str=''):
    with client:
            if name[0] == '/':
                client.mkdir(name)
            else:
                client.mkdir(path + "/" + name)


def download(path: str=''): 
    with client:
        client.download(f'{this_dir}', f'C:\\Users\\Fayaz\\Python\\downloads\\{this_dir.split('/')[-1]}')


def move_file(path:str=''):
    global this_dir
    with client:
        client.move(this_dir, path)
        this_dir = path


def remove(path:str=''):
    global this_dir
    with client:
        client.remove(this_dir)
        this_dir = '/'.join(this_dir.split('/')[:-1])


def rename(path:str=''):
    global this_dir
    with client:
        client.rename(this_dir, path)
        this_dir = path

def exit():
    with client:
        client.close()


def upload(file_name:str=''): 
    with client:
        client.upload(file_name, this_dir+"/"+file_name, overwrite=True)


if __name__ == "__main__":
    print(look_dir(this_dir))
    while True:
        try:
            parts = input(f"{this_dir}: ").strip().split(" ", 1)

            command = parts[0]
            path_to = parts[1] if len(parts) > 1 else ""

            if command == "cd":
                change_dir(path_to)

            if command == 'ls':
                print(look_dir(this_dir))

            if command == 'mkdir':
                mk_dir(this_dir, path_to)

            if command == 'download':
                download(path_to)

            if command == 'move':
                move_file(path_to)

            if command == 'del':
                remove(path_to)

            if command == 'rename':
                rename(path_to)

            if command == 'exit':
                exit()
                break

            if command == 'upl':
                upload(path_to)


        except yadisk.exceptions.PathNotFoundError as e:
            print(e)
            
        except Exception as e:
            print(e)



    
