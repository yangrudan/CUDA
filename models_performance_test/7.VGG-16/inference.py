import torch
import torch.nn as nn
from torchvision import datasets, transforms, models

# 定义数据转换
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 将 28x28 调整为 224x224 适用于 VGG-16
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x.repeat(3, 1, 1)),  # 将单通道转换为三通道
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST 数据集标准化参数
])

# 加载测试数据集
test_dataset = datasets.MNIST(root='../data', train=False, download=False, transform=transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=2)

# 加载 VGG-16 模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.vgg16(weights=None)
model.classifier[6] = nn.Linear(model.classifier[6].in_features, 10)  # MNIST 有 10 个类别
model.load_state_dict(torch.load('vgg16_mnist.pth',weights_only=True))
model.eval()
model = model.to(device)

# 推理
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Accuracy of the network on the test images: {100 * correct / total:.2f}%')
