import pytest
from playwright.sync_api import Page, expect

from tests.pages.TODOMVC.todo_react_page import TodoPage

@pytest.fixture(scope="function")
def todo_page(page: Page):
    """Start each test on the TodoMVC page."""
    return TodoPage(page).navigate()

class TestTodo:
    """Tests for the TodoMVC page."""

    class TestStructure:
        """Tests for the TodoMVC page structure."""

        def test_has_title(self, todo_page: TodoPage):
            """Test that the TodoMVC page has the correct title."""
            # Expect a title "to contain" a substring.
            expect(todo_page.page).to_have_title("React • TodoMVC")

        def test_todo_input_placeholder(self, todo_page: TodoPage):
            """Test that the todo input placeholder is correct."""

            # Expect the todo input placeholder to be correct.
            expect(todo_page.entry).to_have_attribute("placeholder", "What needs to be done?")

    class TestAdd:
        """Tests for adding todo items."""

        @pytest.mark.parametrize("todos", (["a", "b", "c"],))
        def test_add_todos(self, todo_page: TodoPage, todos):
            """Test that todo items can be added."""

            # Expect the list to not exist.
            expect(todo_page.entries).not_to_be_attached()

            # Add todo items.
            todo_page.add(*todos)

            # Expect the todo list to have the added items.
            expect(todo_page.entries).to_have_text(todos)

        def test_todos_are_incomplete_when_added(self, todo_page: TodoPage):
            """Test that todo items are incomplete by default."""

            # Add a todo item.
            todo_page.add("a")

            # Expect the toggle all checkbox to be available.
            expect(todo_page.toggle_all_checkbox).to_be_attached()

            # Expect the toggle all checkbox to be unchecked.
            expect(todo_page.toggle_all_checkbox).not_to_be_checked()

            # Expect the todo item to be incomplete.
            expect(todo_page.get_single_todo_item("a")).not_to_have_class("completed")

    class TestComplete:
        """Tests for the toggle all checkbox."""

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

        class TestCompleteAll:
            """Tests for the toggle all checkbox."""

            def test_toggle_unavailable_when_empty(self, todo_page: TodoPage):
                """Test that the toggle all checkbox is unavailable when there are no todo items."""

                # Expect the toggle all checkbox to not be available.
                expect(todo_page.toggle_all_checkbox).not_to_be_attached()

            @pytest.mark.parametrize("all_todos", (["a"], ["a", "b", "c"]))
            def test_toggle_available_when_at_least_one(self, todo_page: TodoPage, all_todos):
                """Test that the toggle all checkbox is available when there is one or more todo items."""

                # Add a todo item.
                todo_page.add(*all_todos)

                # Expect the toggle all checkbox to be available.
                expect(todo_page.toggle_all_checkbox).to_be_attached()

            @pytest.mark.parametrize("all_todos", (["a", "b", "c"],))
            def test_complete_all_from_zero(self, todo_page: TodoPage, all_todos):
                """Test that todo items can be completed."""

                # Add todo items.
                todo_page.add(*all_todos)

                # Expect all todo items to NOT be completed.
                expect(todo_page.get_completed_todos()).to_have_count(0)

                # Complete all todo items.
                todo_page.toggle_all()

                # Expect all todo items to be completed.
                expect(todo_page.get_completed_todos()).to_have_count(len(all_todos))

                # Ensure all entries are the same amount as completed.
                expect(todo_page.entries).to_have_count(len(all_todos))

            @pytest.mark.parametrize("all_todos", (["a", "b", "c"],))
            def test_complete_all_from_partial(self, todo_page: TodoPage, all_todos):
                """Test that todo items can be completed, when there are already some completed."""

                # Add todo items.
                todo_page.add(*all_todos)

                # Expect all todo items to NOT be completed.
                expect(todo_page.get_completed_todos()).to_have_count(0)

                # Complete the last 2 todo items.
                todo_page.complete(*all_todos[1:])

                # Expect all todo items to be completed.
                expect(todo_page.get_completed_todos()).to_have_count(2)

                # Toggle all todo items.
                todo_page.toggle_all()

                # Expect all todo items to be completed.
                expect(todo_page.get_completed_todos()).to_have_count(len(all_todos))

            @pytest.mark.parametrize("all_todos", (["a", "b", "c"],))
            def test_toggle_all_resets_all(self, todo_page: TodoPage, all_todos):
                """Test that the toggle all checkbox resets all todo items."""

                # Add todo items.
                todo_page.add(*all_todos)

                # Expect all todo items to NOT be completed.
                expect(todo_page.get_completed_todos()).to_have_count(0)

                # Toggle all todo items.
                todo_page.toggle_all()

                # Expect all todo items to be completed.
                expect(todo_page.get_completed_todos()).to_have_count(len(all_todos))

                # Toggle all todo items.
                todo_page.toggle_all(checked=False)

                # Expect all todo items to NOT be completed.
                expect(todo_page.get_completed_todos()).to_have_count(0)
