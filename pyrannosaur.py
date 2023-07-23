from os import getcwd, listdir
from os.path import join, exists
from sys import exit

from markdown import markdown
from jinja2 import Environment, PackageLoader, select_autoescape


class ContentGenerator:
    '''
    Generates content such as directories, pages, links and templates within
    .html files for new posts in a new or existing pyrannosaur website.
    '''

    def __init__(self) -> None:
        self.dm = DirectoryManager()
        self.tl = TemplateLoader()
        self.fm = FileManager()

    # md/html functions

    def convert_markdown_to_html(self) -> None:
        self.dm.check_for_valid_directory()
        '''
        Go through /posts and convert any .md files to .html files.
        '''
        # build file names
        md_files: list[str] = []
        for file in listdir("posts"):
            if file.split(".")[-1] == "md":
                md_files.append(file)

        html_files: list[str] = []
        for file in md_files:
            html_files.append(file.split(".")[0] + ".html")

        # read the files
        md_content: list[str] = []
        for file in md_files:
            md_content.append(markdown(self.fm.read_from_file("posts", file)))

        # write the files
        for i, file in enumerate(html_files):
            self.fm.write_to_file(
                "archive", file,
                self.tl.base_template.render(title=f"Post {i}",
                                             content=md_content[i]))


class FileManager:
    '''
    Performs basic io for files such as reading and writing.
    '''

    def __init__(self) -> None:
        pass

    def write_to_file(self, dir: str, file: str, operation) -> None:
        with open(join(dir, file), 'w') as f:
            f.write(operation)
            f.close()

    def read_from_file(self, dir: str, file: str) -> list[str]:
        with open(join(dir, file), 'r') as f:
            data: str = f.read()
            f.close()
        return data


class DirectoryManager:
    '''
    Manages directories in a pyrannosaur website.
    '''

    def __init__(self) -> None:
        '''
        Initialise if posts/templates directories exist if they don't exist
        then you are in an invalid directory.
        '''
        self.BASE_URL: str = getcwd()
        self.POST_URL: str = join(self.BASE_URL, 'posts') if exists(
            join(self.BASE_URL, 'posts')) else None
        self.TEMPLATE_URL: str = join(self.BASE_URL, 'templates') if exists(
            join(self.BASE_URL, 'templates')) else None

    def check_for_valid_directory(self) -> None:
        '''
        Check if you are in a valid directory.
        A valid directory is one containing /posts and /templates directories.
        If invalid, the program can exit so that a valid directory can be used.
        Function called whenever modifying or generating new posts/pages to
        prevent unneccesary errors or file read/writes.
        '''
        if self.POST_URL is None or self.TEMPLATE_URL is None:
            print(
                "The directory does not contain a /posts or /templates directory"
            )
            print(
                "Check the directory path is correct and run the script again."
            )
            exit(0)


class TemplateLoader:
    '''
    Defines and loads templates for a pyrannosaur website.
    '''

    def __init__(self) -> None:
        self.env = Environment(loader=PackageLoader("pyrannosaur"),
                               autoescape=select_autoescape())
        self.base_template = self.env.get_template("base.html")


cg = ContentGenerator()
cg.convert_markdown_to_html()
