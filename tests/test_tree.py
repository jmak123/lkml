import pytest
from lkml.tree import (
    BlockNode,
    ListNode,
    PairNode,
    SyntaxToken,
    QuotedSyntaxToken,
    ExpressionSyntaxToken,
)


@pytest.mark.parametrize(
    "token_class,expected",
    [
        (SyntaxToken, "foo"),
        (QuotedSyntaxToken, '"foo"'),
        (ExpressionSyntaxToken, "foo ;;"),
    ],
)
def test_syntax_token_str_should_return_formatted(token_class, expected):
    assert str(token_class("foo")) == expected


def test_pair_node_str_should_return_formatted():
    node = PairNode(key=SyntaxToken("foo"), value=SyntaxToken("bar"))
    assert str(node) == "foo:bar"


def test_list_node_str_should_return_formatted():
    # Test a node with PairNodes as items
    node = ListNode(
        type=SyntaxToken("filters"),
        items=(
            PairNode(SyntaxToken("created_date"), QuotedSyntaxToken("7 days")),
            PairNode(SyntaxToken("user.status"), QuotedSyntaxToken("-disabled")),
        ),
    )
    assert str(node) == 'filters:[created_date:"7 days",user.status:"-disabled"]'

    # Test a node with SyntaxTokens as items
    node = ListNode(
        type=SyntaxToken("fields"),
        items=(SyntaxToken("user.user_id"), SyntaxToken("user.age")),
    )
    assert str(node) == "fields:[user.user_id,user.age]"


def test_block_node_str_should_return_formatted():
    node = BlockNode(
        type=SyntaxToken("set"),
        items=(
            ListNode(
                type=SyntaxToken("fields"),
                items=(SyntaxToken("user.user_id"), SyntaxToken("user.age")),
            ),
        ),
        name=SyntaxToken("user_dimensions"),
    )
    assert str(node) == "set:user_dimensions{fields:[user.user_id,user.age]}"


def syntax_token_with_trivia_str_should_render():
    token = SyntaxToken("foo", prefix="# Skip this\n  ")
    assert str(token) == "# Skip this\n  foo"

    token = SyntaxToken("foo", suffix="\n# Skip this\n  ")
    assert str(token == "foo\n# Skip this\n  ")

    token = SyntaxToken("foo", prefix="\n\t", suffix="\t\n")
    assert str(token) == "\n\tfoo\t\n"
