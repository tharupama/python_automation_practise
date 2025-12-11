import os
from pathlib import Path
import shutil
import logging
from datetime import datetime

logging.basicConfig( # describe how logging work
    level=logging.INFO,
    format="%(asctime)s - %levelname)s - %(message)s",#assci time, level name, actual message
    handlers =[
        logging.FileHandler("file_organize.log"),# saves the logging information file named file_organize.log
        logging.StreamHandler()# show logs in console
    ]
)
logger = logging.getLogger(__name__)#create logger object current file module.__name__ special variable that holds the name of the current file/module

File_Categories = {
    "image": [".jpg",".jpeg",".png",".gif",".bmp",".tiff",".svg"],
    "video": [".mp4",".mkv",".flv",".avi",".mov",".wmv"],
    "document": [".pdf",".doc",".docx",".xls",".xlsx",".ppt",".pptx",".txt",".odt",".rtf"],
    "audio": [".mp3",".wav",".aac",".flac",".ogg",],
    "archive": [".zip",".rar",".tar",".gz",".7z"],
    "code": [".py",".js",".html",".css",".java",".c",".cpp",".rb",".php",".go",".rs"],
    "executable": [".exe",".bat",".sh",".bin",".msi"],
    "data": [".csv",".json",".xml",".yaml",".yml",".db",".sql"]
}
def get_category(File_extension):
    for category, extensions in File_Categories.items():
        if File_extension.lower() in extensions:
            return category
    return "Additional"

def create_category_folder(directory, categories):
    for category in categories:
        category_path = os.path.join(directory, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            logger.info(f"Created folder {category_path}")

def organize_files(sourse_dir, organize_by="category"):
    if not os.path.exists(sourse_dir):
        logger.error(f"The directory {sourse_dir} does not exist.")
        return

    files = [f for f in os.listdir(sourse_dir)#list every thing in directore both files and folders.Example output: ['photo.jpg', 'Documents', 'video.mp4', 'Music']
             if os.path.isfile(os.path.join(sourse_dir, f))]#combine directory path with the file name to cteate full path and check if its a file

            # issella ekin eka f walata assign karanawa if condition ekak dala chek karana nisa. ita passe file kiyanekata include wenne directory
            # ekayi ara namayi ekathu karama full patheka file path ekaknam witharayi.
    #file ekakda nadda balanna path ekath ekka denna one nisa thamayi ekathu karanne., files walata assign wenne path eka nathuwa namayi ext ekayi
    if not files:
        logger.info("No files found to organize")
        return
    logger.info(f"Found {len(files)} files to organize")

    if organize_by == "category":
        organize_by_category(sourse_dir, files)
    elif organize_by == "extension":
        organize_by_extension(sourse_dir, files)
    elif organize_by == "date":
        organize_by_date(sourse_dir, files)
    else:
        logger.error(f"Unknown organize_by option: {organize_by}")

def organize_by_category(sourse_dir, files):
    categories = set()
    for file in files:
        _, extension = os.path.splitext(file)#undescore eken kiyanne file eke namayi extension ekayi wen unahama palaweni value eka e kiyanne nama one na kiyala deveni value ekata extension eka assign wenawa.
        category = get_category(extension)#get category function eka call karanawa, category eka ganna extension ekata adala.
        categories.add(category)#categories kiyana set ekata add karanawa category eka, list ekak ganne nathuwa set ekak gaththe set ekedi duplicate value ignore karana nisa.
        #naththan ekama category ekata folder dekathunak hadenna puluwan.

    create_category_folder(sourse_dir, categories)
    for file in files:
        file_path = os.path.join(sourse_dir, file)
        _, extension = os.path.splitext(file)
        category = get_category(extension)

        dest_path = os.path.join(sourse_dir, category)
        dest_path = os.path.join(dest_dir, file)

        try:
            if os.path.exists(dest_path):
                base,ext = os.path.splittext(file)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{base}_{timestamp}{ext}"
                dest_path = os.path.join(dest_dir, new_filename)

                shutil.move(file_path, dest_path)
                logger.info(f"Moved {file} to {category} folder")
        except Exception as e:
            logger.error(f"Error moving file {file}: {str(e)}")

def organize_by_extension(sourse_dir, files):
    extention = set()
    for file in files:
        _, ext = os.path.splitext(file)
        if ext:
            extention.add(ext.lower())
    for ext in extentions:
        ext_folder = os.path.join(sourse_dir, ext[1:])#remove dot from extension
        if not os.path.exists(ext_folder):
            os.makedir(ext_folder)

    for file in files:
        file_path = os.path.join(sourse_dir, file)
        _, ext = os.path.splitext(file)
        if ext:
             ext_folder = os.path.join(sourse_dir, ext[1:])
             dest_path = os.path.join(ext_folder, file)

             try:
                 if os.path.exists(dest_path):
                     base, ext_part = os.path.splitext(file)
                     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                     new_filename = f'{base}_{timestamp}{ext_part}'
                     dest_path = os.path.join(ext_folder, new_filename)

                 shutil.move(file_path, dest_path)
                 logger.info(f"Moved {file} to {ext[1:]} folder")
             except Exception as e:
                    logger.error(f"Error moving file {file}: {str(e)}")

def organize_by_date(sourse_dir, files):
    for file in files:
        file_path = os.path.join(sourse_dir, file)

        creation_time = os.path.getctime(file_path)
        date_obj = datetime.fromtimestamp(creation_time)
        date_folder = date_obj.strftime("%Y-%m-%d")

        date_dir = os.path.join(sourse_dir, date_folder)
        if not os.path.exists(date_dir):
            os.makedirs(date_dir)

        dest_path = os.path.join(date_dir, file)
        try:
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(file)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{base}_{timestamp}{ext}"
                dest_path = os.path.join(date_dir, new_filename)

            shutil.move(file_path, dest_path)
            logger.info(f"Moved {file} to {date_folder} folder")
        except Exception as e:
            logger.error(f"Error moving file {file}: {str(e)}")

def search_files(directory, search_term, search_by="name"):
    if not os.path.exists(directory):
        logger.error(f"The directory {directory} does not exist.")
        return []
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            if search_by == "name":
                if search_term.lower() in file.lower():
                    matching_files.append(file_path)
            elif search_by == "extension":
                _, ext = os.path.splitext(file)
                if search_term.lower() in ext.lower():
                    matching_files.append(file_path)

                elif search_by == "content":
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            if search_term.lower() in content.lower():
                                matching_files.append(file_path)
                    except:
                        continue

    return matching_files


def main():
    current_directory = os.getcwd()
    target_directory = current_dir

    print("file organizer script")
    print("==========")
    print(f"Target directory :{target_directory}")
    print()

    print("searching for files...")
    pdf_files = search_files(target_dir, ".pdf", search_by="extension")
    print(f"Found {len(pdf_files)} PDF files.")
    for file in pdf_files:
        print(f"-{file}")

    print()

    print("organizing files by category...")
    organize_files(target_dir, organize_by="category")

    print()
    print("organization completed! check log in your terminal")

    if __name__ == "__main__":
        main()




