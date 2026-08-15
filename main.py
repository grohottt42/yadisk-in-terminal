import yadisk
from dotenv import load_dotenv
import os

load_dotenv()

current_path = '/Книги/Квант/2011'
path_to = ''
TOKEN = os.getenv("TOKEN")

client = yadisk.Client(token=f"{TOKEN}")


def look_dir(path: str='') -> list:
    with client:
        return [book.name for book in list(client.listdir(f'{path}'))]


def change_dir(path: str=''):
    global current_path
    with client:
        parts = []
        for part in path.split('/'):
            parts.append(part)

        if parts[0] == '':
            current_path = '/'
            parts.pop(0)
        
        for part_dir in parts:
            if part_dir == '..':
                current_path = '/'.join(current_path.split('/')[:-1]) 
                current_path = '/' if current_path == '' else current_path
            elif part_dir == '':
                continue
            elif part_dir == '.':
                continue 
            else:
                if client.exists(current_path.strip('/') + '/' + part_dir) and client.is_dir(current_path.strip('/') + '/' + part_dir): 
                    current_path = current_path.strip('/') + '/' + part_dir  


def mk_dir(path: str='', name: str=''):
    with client:
            if name[0] == '/':
                client.mkdir(name)
            else:
                client.mkdir(path + "/" + name)


def download(path: str=''): 
    file_name, dest_path = path.rsplit(' ', 1)
    with client:
        if file_name[0] =='/':
            client.download(file_name, dest_path)
        else:
            client.download(current_path + '/' + file_name, dest_path)


def move_file(path:str=''):
    global current_path
    with client:
        client.move(current_path, path)
        current_path = path


def remove(path:str=''):
    global current_path
    with client:
        if client.exists(current_path + '/' + path):     
            client.remove(current_path + '/' + path)
        else:
            print('Such a file or directory does not exist.')


def rename(path:str=''):
    global current_path
    with client:
        client.rename(current_path, path)
        current_path = path


def exit():
    with client:
        client.close()


def upload(file_name:str=''): 
    with client:
        client.upload(file_name, current_path+"/"+file_name, overwrite=True)


if __name__ == "__main__":
    print(look_dir(current_path))
    while True:
        try:
            parts = input(f"disk:{current_path}: ").strip().split(" ", 1)

            command = parts[0]
            argument = parts[1] if len(parts) > 1 else ""

            if command == "cd":
                change_dir(argument)

            if command == 'ls':
                print(look_dir(current_path))

            if command == 'mkdir':
                mk_dir(current_path, argument)

            if command == 'download':
                download(argument)

            if command == 'move':
                move_file(argument)

            if command == 'rm':
                remove(argument)

            if command == 'rename':
                rename(argument)

            if command == 'exit':
                exit()
                break

            if command == 'upl':
                upload(argument)


        except yadisk.exceptions.PathNotFoundError as e:
            print(e)
            
        except Exception as e:
            print(e)

    
