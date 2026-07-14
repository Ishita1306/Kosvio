"""
Glass card component.

Provides a styled container with glassmorphic backdrop filter and borders,
supporting dark theme aesthetics.
"""

import streamlit as st


def render_glass_card(content_html: str, class_name: str = "") -> None:
    """
    Render a premium glassmorphic card containing static HTML content.

    Args:
        content_html (str): The HTML content to render inside the card.
        class_name (str): Additional CSS classes to append.
    """
    card_html = f'<div class="glass-card {class_name}">{content_html}</div>'
    st.markdown(card_html, unsafe_allow_html=True)


def glass_card_wrapper_start(style_attrs: str = "") -> None:
    """
    Inject structural opening tag for custom styled HTML containers.

    Args:
        style_attrs (str): Inline CSS style attributes.
    """
    st.markdown(
        f'<div class="glass-card" style="padding: 1.5rem; border-radius: 14px; margin-bottom: 1rem; {style_attrs}">',
        unsafe_allow_html=True,
    )


def glass_card_wrapper_end() -> None:
    """Inject closing tag for custom styled HTML containers."""
    st.markdown("</div>", unsafe_allow_html=True)
