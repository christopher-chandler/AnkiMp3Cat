# Standard
# None

# Pip
# None

# Custom
from app_resources.mp3_combiner import Mp3Combiner

yaml_file_data = r"path to epsiode_information .yml file"
combiner = Mp3Combiner(show_yaml_data=yaml_file_data)
combiner.combine_files(find_hook=False)
