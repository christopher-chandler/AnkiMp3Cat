# Standard
import glob
import io
import logging
import os
import re
import shutil
import time


# Pip
import eyed3
import yaml

# Custom
from progbar import update_progress


class Mp3Combiner:
    """ """

    def __init__(self, show_yaml_data):
        """

        :param show_yaml_data:
        """
        self.anki_app_data = show_yaml_data

    def __open_yaml_data(self) -> dict:
        """

        :return:
        """
        with open(self.anki_app_data, mode="r",encoding="utf-8") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
            return yaml_data

    def __change_directory(self) -> None:
        """

        :return:
        """
        path = self.__open_yaml_data().get("anki_media")
        os.chdir(path)

    def __delete_files(self, temp):
        try:
            files = glob.glob(fr"{temp}\*")
            for f in files:
                os.remove(f)
        except:
            pass

    def file_type_search(self) -> list:
        """
        :return:
            file_format_results (list) a collection of the shows in the Anki directory.
        """
        self.__change_directory()
        yml_data = self.__open_yaml_data()
        show_name = yml_data.get("show_name")
        file_format = yml_data.get("file_format")

        # Adding all files of the specified file type to the collection.
        file_format_results = list()
        for file_type in glob.glob(f"*.{file_format}"):
            if show_name in file_type:
                file_format_results.append(file_type)

        return file_format_results

    def episode_collection(self):
        """ """
        yml_data = self.__open_yaml_data()

        key_location = yml_data.get("episode_index")
        show = self.file_type_search()
        episode_keys = {episode[:key_location] for episode in show}

        episode_files = {key: set() for (key) in episode_keys}

        for episode in episode_files:
            for file in show:
                if episode == file[:key_location]:
                    episode_files[episode].add(file)

        return episode_files

    def __add_meta_data(self, file, track_num, title):
        data = self.__open_yaml_data()

        # Standard ID3 data
        log_stream = io.StringIO()
        logging.basicConfig(stream=log_stream, level=logging.INFO)
        audio_file = eyed3.load(file)
        llog = log_stream.getvalue()
        if llog:
            log_stream.truncate(0)
        audio_file.initTag()

        audio_file.tag.title = title
        audio_file.tag.track_num = track_num
        audio_file.tag.artist = data.get("show_name")
        audio_file.tag.album = data.get("show_name")
        audio_file.tag.genre = data.get("genre")

        cover_art_filename = self.__open_yaml_data().get("cover_art")

        with open(cover_art_filename, "rb") as cover_art:
            audio_file.tag.images.set(0, cover_art.read(), "image/jpg")

        audio_file.tag.save()

        return audio_file

    def combine_files(self, find_hook: bool) -> None:
        """

        :return:
        """

        # combines the files and moves them to the desired destination
        show_collection = self.episode_collection()
        anki_media = self.__open_yaml_data().get("anki_media")
        save_path = self.__open_yaml_data().get("save_path")
        show_name = self.__open_yaml_data().get("show_name")
        temp_folder = self.__open_yaml_data().get("temp_folder")
        mp3_cat = self.__open_yaml_data().get("mp3_cat")
        show_amount = len(show_collection)
        track_num = 0

        for episode_name in sorted(show_collection):

            track_num += 1
            prog_amount = float(track_num / show_amount)
            if find_hook is False:
                update_progress(label=episode_name, progress=prog_amount)
            else:
                update_progress(label=f"Possible hook for {episode_name}", progress=1)

            episode_collection = sorted(show_collection.get(episode_name))

            if os.path.exists(temp_folder) is False:
                os.mkdir(temp_folder)

            for file in episode_collection:
                os.chdir(anki_media)
                shutil.copy(file, rf"{temp_folder}\{file}")

            time.sleep(2)

            # Execute mp3cat in the temp directory
            os.chdir(temp_folder)
            os.popen(rf"{mp3_cat} {episode_name}.mp3")

            time.sleep(3)

            self.__add_meta_data(
                file=episode_name + ".mp3", track_num=track_num, title=episode_name
            )

            if os.path.exists(rf"{temp_folder}\{episode_name}.mp3"):
                shutil.copy(
                    rf"{temp_folder}\{episode_name}.mp3",
                    rf"{save_path}\{episode_name}.mp3",
                )

            time.sleep(3)
            os.chdir(r"C:\Users\chris\Github\Python\Mp3Combiner")
            shutil.rmtree(temp_folder)

            if find_hook:
                break

        print(f"File combination for {show_name} is now complete.")
        print(f"Please check the directory {save_path}.")

    def show_check(self, file_type: str = "mp3") -> set:
        """

        :param file_type:
        :return:
        """

        self.__change_directory()

        files = set()

        for file in glob.glob(f"*.{file_type}"):
            first_number = re.search(r"\d", file)
            files.add(file[: first_number.start()])

        return files


if __name__ == "__main__":
    yaml_file_data = r"C:\Users\chris\Github\Python\Mp3Combiner\episode_information.yml"
    combiner = Mp3Combiner(show_yaml_data=yaml_file_data)
    combiner.combine_files(find_hook=False)
