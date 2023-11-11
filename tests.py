import unittest
import os
from unittest.mock import patch, call
from pyrannosaur import ContentGenerator, InvalidDirectoryError, DirectoryManager


class TestContentGenerator(unittest.TestCase):
    # ... other test methods ...

    @patch("pyrannosaur.join", side_effect=os.path.join)
    @patch("pyrannosaur.listdir", return_value=["file1.md", "file2.md"])
    @patch("pyrannosaur.markdown", return_value="mocked_html_content")
    @patch("pyrannosaur.FileManager.write_to_file")
    def test_convert_markdown_to_html(
        self, mock_write_to_file, mock_markdown, mock_listdir, mock_join
    ):
        cg = ContentGenerator()

        # Mock FileManager's read_from_file method
        with patch(
            "pyrannosaur.FileManager.read_from_file",
            return_value="mocked_markdown_content",
        ):
            cg.convert_markdown_to_html()

        # Assertions
        expected_calls = [
            call(
                "html/posts",
                "file1.html",
                cg.tl.base_template.render(
                    title="file1.html", content="mocked_html_content"
                ),
            ),
            call(
                "html/posts",
                "file2.html",
                cg.tl.base_template.render(
                    title="file2.html", content="mocked_html_content"
                ),
            ),
            call(
                "html",
                "index.html",
                cg.tl.index_template.render(
                    title="Site Index",
                    archive=[
                        '<a href="posts/file1.html">file1</a>',
                        '<a href="posts/file2.html">file2</a>',
                    ],
                ),
            ),
        ]
        mock_write_to_file.assert_has_calls(expected_calls, any_order=False)

    def test_invalid_directory_error(self):
        try:
            dm = DirectoryManager()
            dm.check_for_valid_directory()
        except InvalidDirectoryError:
            pass


if __name__ == "__main__":
    unittest.main()
