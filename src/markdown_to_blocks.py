from textnode import (
    TextNode,
    TextType    
)
from inline_markdown import split_nodes_image, split_nodes_link


def text_to_textnodes(text):
    # Initialize with a single text node containing all the raw text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply bold delimiters first
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Apply italic delimiters
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # Apply code block delimiters
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Extract and split images
    nodes = split_nodes_image(nodes)
    
    # Extract and split links
    nodes = split_nodes_link(nodes)
    
    return nodes


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(old_node)
            continue
        
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Missing closing delimiter" in str(context.exception))
        
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TEXT_TYPE_TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
                
    return new_nodes


# --- Helper functions for images/links ---
def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
            
        for image_alt, image_url in images:
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid image syntax")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TEXT_TYPE_TEXT))
            new_nodes.append(TextNode(image_alt, TEXT_TYPE_IMAGE, image_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TEXT_TYPE_TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
            
        for link_text, link_url in links:
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid link syntax")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TEXT_TYPE_TEXT))
            new_nodes.append(TextNode(link_text, TEXT_TYPE_LINK, link_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TEXT_TYPE_TEXT))
            
    return new_nodes
    


