import pytest
from playwright.sync_api import Page, expect

from tests.pages.todo_react_page import TodoPage

@pytest.fixture(scope="function")
def todo_page(page: Page):
    """Start each test on the TodoMVC page."""
    todo_page = TodoPage(page)
    todo_page.navigate()
    return todo_page

class TestTodo:
    """Tests for the TodoMVC page."""

    class TestTodo:

        def test_has_title(self, todo_page: TodoPage):
            """Test that the TodoMVC page has the correct title."""
            # Expect a title "to contain" a substring.
            expect(todo_page.page).to_have_title("React • TodoMVC")

        def test_todo_input_placeholder(self, todo_page: TodoPage):
            """Test that the todo input placeholder is correct."""

            # Expect the todo input placeholder to be correct.
            expect(todo_page.entry).to_have_attribute("placeholder", "What needs to be done?")

        def test_add_todos(self, todo_page: TodoPage):
            """Test that todo items can be added."""

            # Expect the list to not exist.
            expect(todo_page.entries).not_to_be_attached()

            # Add todo items.
            todo_page.add("a", "b", "c")

            # Expect the todo list to have the added items.
            expect(todo_page.entries).to_have_text(["a", "b", "c"])

        @pytest.mark.parametrize(
            "all_todos, todo_to_complete",
            (
                (["a", "b", "c"], "a"),
                (["a", "b", "c"], "b"),
                (["d", "b", "c"], "c"),
            )
        )
        def test_complete_one_todo(self, todo_page: TodoPage, all_todos, todo_to_complete):
            """Test that todo items can be completed."""

            # Add todo items.
            todo_page.add(*all_todos)

            # Expect all todo items to NOT be completed.
            expect(todo_page.get_completed_todos()).to_have_count(0)

            # Complete todo item "b".
            todo_page.complete(todo_to_complete)

            # Expect the first todo item to be completed.
            expect(todo_page.get_completed_todos()).to_have_count(1)

            # Let's ensure it's the correct todo item.
            expect(todo_page.get_single_todo_item(todo_to_complete)).to_have_class("completed")

    class TestTodoToggleAll:
        """Tests for the toggle all checkbox."""

        @pytest.mark.parametrize("all_todos", (["a", "b", "c"],))
        def test_complete_all_from_zero(self, todo_page: TodoPage, all_todos):
            """Test that todo items can be completed."""

            # all_todos = ["a", "b", "c"]

            # Add todo items.
            todo_page.add(*all_todos)

            # Expect all todo items to NOT be completed.
            expect(todo_page.get_completed_todos()).to_have_count(0)

            # Complete all todo items.
            todo_page.toggle_all()

            # Expect all todo items to be completed.
            expect(todo_page.get_completed_todos()).to_have_count(len(all_todos))
