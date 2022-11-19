# import standard
import sys

# pip
# None

# Custom
# None


def update_progress(label: str, progress: float, bar_length: int = 10) -> None:
    """

    :param label (str): The title of the progress bar
    :param progress ():
    :param bar_length:

    :return:
    """

    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"

    block = int(round(bar_length * progress))

    bar = "#" * block + "-" * (bar_length - block)
    percent = round(progress * 100, 2)

    text = f"\r{label}:[{bar}] % {percent} {status}"
    sys.stdout.write(text)
    sys.stdout.flush()
