# LightModal là gì?
LightModal là một utility giúp bạn khởi tạo và xử lý dữ liệu từ Discord Modal một cách nhanh chóng chỉ với vài dòng code. Bạn không cần phải viết class kế thừa ``discord.ui.Modal`` hay tự quản lý logic `on_submit`, `on_timeout`, `on_error` phức tạp.

# Tham số 
trước khi đọc cách sử dụng, bạn nên coi qua tham số của các method lightmodal cung cấp 

---

### 1. Tham số của Class `LightModal`

| Tham số | Kiểu dữ liệu | Mặc định | Mô tả |
| --- | --- | --- | --- |
| `modal_title` | `str` | *Bắt buộc* | Tiêu đề hiển thị ở phía trên cùng của Modal. |
| `timeout` | `float` | `300.0` | Thời gian tối đa (tính bằng giây) chờ người dùng gửi form trước khi hết hạn. |

---

### 2. Tham số của method `add_field()`

| Tham số | Kiểu dữ liệu | Mặc định | Mô tả |
| --- | --- | --- | --- |
| `field_or_label` | `Union[TextInput, str]` | *Bắt buộc* | Nhãn (Label) hiển thị trên ô nhập, hoặc truyền trực tiếp một object `discord.ui.TextInput`. |
| `placeholder` | `Optional[str]` | `None` | Chữ mờ gợi ý hiển thị bên trong ô nhập khi chưa gõ gì. |
| `default` | `Optional[str]` | `None` | Văn bản/giá trị được điền sẵn trong ô nhập. |
| `style` | `discord.TextStyle` | `TextStyle.short` | Dạng ô nhập (`short` cho 1 dòng, `paragraph` cho nhiều dòng). |
| `min_length` | `Optional[int]` | `None` | Số lượng ký tự tối thiểu người dùng phải nhập. |
| `max_length` | `Optional[int]` | `None` | Số lượng ký tự tối đa người dùng có thể nhập. |
| `required` | `bool` | `True` | Quy định ô nhập này có bắt buộc điền hay không (`True`/`False`). |
| `row` | `Optional[int]` | `None` | Thứ tự dòng hiển thị ô nhập trong Modal (từ `0` đến `4`). |

---

### 3. Tham số của method `show()`

| Tham số | Kiểu dữ liệu | Mặc định | Mô tả |
| --- | --- | --- | --- |
| `interaction` | `discord.Interaction` | *Bắt buộc* | Object interaction của Discord để gửi Modal tới người dùng. |

# Cách sử dụng

## 1. Ví dụ cơ bản

```python 
from deesyn_utils import LightModal
import discord

@bot.tree.command(name="example", description="Ví dụ mẫu về lightmodal")
async def feedback(interaction: discord.Interaction):
    # Khởi tạo LightModal
    modal = LightModal(modal_title="Example", timeout=180.0)

    # Thêm các field
    # Các đối số của add_field same với discord.TextInput()
    modal.add_field("Tiêu đề", placeholder="Nhập tiêu đề ở đây...")
    modal.add_field(
        "Nội dung",
        style=discord.TextStyle.paragraph,
        placeholder="placeholder",
        required=True
    )
    
    # để hiện modal cho người dùng bạn cần sử dụng method .show và truyền interaction vào
    result = await modal.show(interaction)

    # Kiểm tra nếu user bị timeout hoặc đóng modal
    if not result:
        return

    # Lấy giá trị trả về (dict dạng {label: value})
    title = result.get("Tiêu đề")
    content = result.get("Nội dung")

    await interaction.followup.send(f"Đã nhận feedback:\n**{title}**: {content}")
```

## 2. Sử dụng chaining 
Bạn có thể nối các phương thức ``.add_field()`` liên tiếp nhau:

```python 
result = await (
    LightModal("Đăng ký thông tin")
    .add_field("Họ và tên")
    .add_field("Email", placeholder="example@gmail.com")
    .add_field("Tuổi", min_length=1, max_length=3)
    .show(interaction)
)

if result:
    name = result.get("Họ và tên")
    email = result.get("Email")
    age = result.get("Tuổi")
```

## 3. Sử dụng ``discord.ui.TextInput`` 

Ngoài việc truyền string label, bạn cũng có thể tự khởi tạo ``TextInput`` rồi truyền thẳng vào:

```python 
custom_input = discord.ui.TextInput(
    label="Mô tả bản thân",
    style=discord.TextStyle.long,
    default="Tôi là..."
)

modal = LightModal("Hồ sơ cá nhân")
modal.add_field(custom_input)

result = await modal.show(interaction)
```
