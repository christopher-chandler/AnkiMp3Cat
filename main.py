# Standard
# None

# Pip
# None

# Custom
from app_resources.mp3_combiner import Mp3Combiner

if __name__ == "__main__":
    yaml_file_data = r"episode_information.yml"
    combiner = Mp3Combiner(show_yaml_data=yaml_file_data)
    combiner.combine_files(find_hook=False)
