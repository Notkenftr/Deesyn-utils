# What is LightModal?

LightModal is a utility from `deesyn-utils` that allows you to quickly create and handle data from Discord Modals in just a few lines of code. You don't need to inherit `discord.ui.Modal` or manage complex logic for `on_submit`, `on_timeout`, or `on_error`.

---

# Parameters

Before jumping into usage examples, check out the parameters accepted by the methods provided by LightModal:

### 1. `LightModal` Class Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `modal_title` | `str` | *Required* | The title displayed at the top of the Modal. |
| `timeout` | `float` | `300.0` | Maximum time (in seconds) to wait for user submission before timing out. |

---

### 2. `add_field()` Method Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `field_or_label` | `Union[TextInput, str]` | *Required* | Label text to display on the input, or an existing `discord.ui.TextInput` object. |
| `placeholder` | `Optional[str]` | `None` | Placeholder text shown inside the input box when empty. |
| `default` | `Optional[str]` | `None` | Pre-filled default text value for the input box. |
| `style` | `discord.TextStyle` | `TextStyle.short` | Input field style (`short` for single-line, `paragraph` for multi-line). |
| `min_length` | `Optional[int]` | `None` | Minimum number of characters allowed. |
| `max_length` | `Optional[int]` | `None` | Maximum number of characters allowed. |
| `required` | `bool` | `True` | Whether this field is mandatory (`True`/`False`). |
| `row` | `Optional[int]` | `None` | Display row order in the Modal (from `0` to `4`). |

---

### 3. `show()` Method Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `interaction` | `discord.Interaction` | *Required* | Discord interaction object used to send the Modal to the user. |

---

# How to Use

## 1. Basic Example

```python
from deesyn_utils import LightModal
import discord

@bot.tree.command(name="example", description="LightModal sample example")
async def feedback(interaction: discord.Interaction):
    # Initialize LightModal
    modal = LightModal(modal_title="Example", timeout=180.0)

    # Add fields
    # Arguments for add_field are identical to discord.ui.TextInput()
    modal.add_field("Title", placeholder="Enter title here...")
    modal.add_field(
        "Content",
        style=discord.TextStyle.paragraph,
        placeholder="placeholder",
        required=True
    )
    
    # Display the modal to the user using the .show method passing the interaction
    result = await modal.show(interaction)

    # Check if user timed out or closed the modal
    if not result:
        return

    # Retrieve values (returns dict formatted as {label: value})
    title = result.get("Title")
    content = result.get("Content")

    await interaction.followup.send(f"Feedback received:\n**{title}**: {content}")

```

## 2. Method Chaining

You can chain multiple `.add_field()` calls together:

```python
result = await (
    LightModal("Registration")
    .add_field("Full Name")
    .add_field("Email", placeholder="example@gmail.com")
    .add_field("Age", min_length=1, max_length=3)
    .show(interaction)
)

if result:
    name = result.get("Full Name")
    email = result.get("Email")
    age = result.get("Age")

```

## 3. Passing `discord.ui.TextInput` Directly

Besides passing a string label, you can also instantiate a `TextInput` object and pass it directly:

```python
custom_input = discord.ui.TextInput(
    label="About Me",
    style=discord.TextStyle.long,
    default="I am..."
)

modal = LightModal("User Profile")
modal.add_field(custom_input)

result = await modal.show(interaction)

```
