from enum import Enum
import unittest
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import HTMLNode
def text_to_children(text):
    # 1. Convert the raw string into a list of TextNode objects
    text_nodes = text_to_textnodes(text)
    
    # 2. Convert each TextNode into its corresponding HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
        
    return html_nodes
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        # Code block: special case, no inline parsing
        if block_type == BlockType.CODE:
            # Extract content without ```
            code_content = block.strip().strip("```").strip()
            text_node = TextNode(code_content, TextType.TEXT)
            code_node = HTMLNode("code", children=[text_node_to_html_node(text_node)])
            block_node = HTMLNode("pre", children=[code_node])
            
        # Paragraphs
        elif block_type == BlockType.PARAGRAPH:
            block_node = HTMLNode("p", children=text_to_children(block))
            
        # Headings (Assumes your block_to_block_type returns "heading" for headers)
        elif block_type == BlockType.heading:
            level = 0
            while block.startswith("#"):
                level += 1
                block = block[1:]
            block = block.strip()
            block_node = HTMLNode(f"h{level}", children=text_to_children(block))
            
        # Unordered lists
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                if line.strip().startswith(("* ", "- ")):
                    # Strip the marker
                    text = line.strip()[2:]
                    items.append(HTMLNode("li", children=text_to_children(text)))
            block_node = HTMLNode("ul", children=items)
            
        # Ordered lists
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                if line.strip():
                    # Strip the "1. " marker
                    text = line.strip().split(". ", 1)[1]
                    items.append(HTMLNode("li", children=text_to_children(text)))
            block_node = HTMLNode("ol", children=items)
            
        # Quotes
        elif block_type == BlockType.QUOTE:
            lines = []
            for line in block.split("\n"):
                if line.strip().startswith(">"):
                    lines.append(line.strip().lstrip(">").strip())
            quote_text = " ".join(lines)
            block_node = HTMLNode("blockquote", children=text_to_children(quote_text))
            
        else:
            raise ValueError(f"Unknown block type: {block_type}")

        children.append(block_node)

    return HTMLNode("div", children=children)
    
def text_to_children(text):
    """
    Converts a raw string of block text into a list of HTML inline nodes
    """
    # Use your brand new function!
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    
    for text_node in text_nodes:
        # text_node_to_html_node converts a single TextNode to a LeafNode 
        # (e.g., TextType.BOLD becomes LeafNode("b", text_node.text))
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
        
    return html_nodes       
    

