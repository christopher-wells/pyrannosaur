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
            with open(join("posts", file), 'r') as f:
                md_content.append(markdown(f.read()))
                f.close()

        # write the files
        for i, file in enumerate(html_files):
            with open(join("html", file), 'w') as f:
                f.write(md_content[i])
                f.close()
    
    def write_to_page_from_template(self, file, title) -> None:
        self.dm.check_for_valid_directory()
        with open(file, 'w') as f:
            f.write(
                self.tl.base_template.render(title=title)
            )
    

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
    Defines and loads templates for pyrannosaur websites.
    '''
    def __init__(self) -> None:
        self.env = Environment(
            loader=PackageLoader("pyrannosaur"),
            autoescape=select_autoescape()
            )
        self.base_template = self.env.get_template("base.html")


cg = ContentGenerator()
cg.convert_markdown_to_html()
cg.write_to_page_from_template("index.html", "Hello World!")