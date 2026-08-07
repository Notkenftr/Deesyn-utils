from __future__ import annotations

import discord
import asyncio
from typing import Optional, Union


class _Modal(discord.ui.Modal):
    __slots__ = ["future","defer"]
    def __init__(self, title: str, future: asyncio.Future, timeout: Optional[float] = None,defer=True):
        super().__init__(title=title, timeout=timeout)
        self.future = future
        self.defer = defer

    async def on_submit(self, interaction: discord.Interaction):
        result = {
            item.label: item.value
            for item in self.children
            if isinstance(item, discord.ui.TextInput)
        }

        if not self.future.done():
            self.future.set_result(result)
        if self.defer:
            await interaction.response.defer()
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        if not self.future.done():
            self.future.set_exception(error)
        if not interaction.response.is_done():
            await interaction.response.defer()
    async def on_timeout(self):
        if not self.future.done():
            self.future.set_exception(asyncio.TimeoutError("The modal has been cancelled or has timed out."))

class LightModal(discord.ui.Modal):
    __slots__ = ["modal_title", "timeout","fields"]
    def __init__(self, modal_title: str, timeout: float = 300.0):
        self.modal_title = modal_title
        self.timeout = timeout
        self.fields: list[discord.ui.TextInput] = []

    def add_field(
            self,
            field_or_label: Union[discord.ui.TextInput, str],
            placeholder: Optional[str] = None,
            default: Optional[str] = None,
            style: discord.TextStyle = discord.TextStyle.short,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            required: bool = True,
            row: Optional[int] = None,
    ) -> "LightModal":
        if len(self.fields) >= 5:
            raise ValueError("Discord Modal chỉ cho phép tối đa 5 fields.")

        if isinstance(field_or_label, discord.ui.TextInput):
            self.fields.append(field_or_label)
        else:
            text_input = discord.ui.TextInput(
                label=field_or_label,
                placeholder=placeholder,
                default=default,
                style=style,
                min_length=min_length,
                max_length=max_length,
                required=required,
                row=row,
            )
            self.fields.append(text_input)

        return self

    async def show(
            self,
            interaction: discord.Interaction
    ) -> dict[str, str]:
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        modal = _Modal(
            title=self.modal_title,
            future=future,
            timeout=self.timeout
        )

        for field in self.fields:
            modal.add_item(field)

        await interaction.response.send_modal(modal)

        try:
            return await future
        except asyncio.TimeoutError:
            return {}