from dataclasses import dataclass


@dataclass
class Product:
  name: str
  price: float
  tool: bool


products = [
  Product("martillo", 50, True),
  Product("destornillador", 20, True),
  Product("sierra", 100, True),
  Product("clavos", 1, False),
  Product("tornillos", 1, False),
  Product("hojas de sierra", 10, False),
]


taxes = {'tool': 10, 'other': 5}

@dataclass
class Discount:
  after: int
  discount: float

discounts = {
  'martillo': Discount(20, 5.0),
  'destornillador': Discount(10, 5.0),
  'clavos': Discount(1000, 5.0),
  'tornillos': Discount(2500, 10.0),
}

order = [
  {'id' : 0, 'q': 20},
  {'id' : 1, 'q': 25},
  {'id' : 2, 'q': 30},
  {'id' : 3, 'q': 3000},
  {'id' : 4, 'q': 5000},
  {'id' : 5, 'q': 20},
]

@dataclass
class Item:
  product: Product
  quantity: int
  discount_applied: float
  tax_applied: float
  amount: float

  def __str__(self):
    return f"\t{self.product.name:15}\t$  {self.product.price:12.1f}\t{self.quantity:8}\t$ {self.amount:8.1f}\t$ {self.discount_applied:8.1f}\t$ {self.tax_applied:8.1f}\t$ {self.amount-self.discount_applied+self.tax_applied:8.1f}"


def show_invoice(order):
  items = []
  for item in order:
    product = products[item['id']]
    quantity = item['q']
    discount = discounts.get(product.name) 
    item = create_item(product, quantity, discount)
    items.append(item)

  print_invoice(items)

def create_item(product, quantity, discount):
  value = quantity * product.price
  tax = find_tax(product, value)
  discount_applied = calc_discount(product, quantity, discount)
  return Item(product, quantity, discount_applied, tax, value)

def calc_discount(product, quantity, discount):
  if discount is None:
    return 0
  delta = quantity - discount.after
  return (product.price * discount.discount/100.0) * delta

def find_tax(product, value):
  if product.tool:
    return value * taxes['tool'] / 100.0
  else:
    return value * taxes['other'] / 100.0

def print_invoice(items):
  print("Factura")
  print("Items:")
  print(f"\t{'Producto':12}\tCosto Unitario\tCantidad\tBruto\t\tDescuento\tImpuesto\tNeto")
  total = 0
  tax = 0
  discount = 0
  for item in items:
    print(item)
    total += item.amount
    tax += item.tax_applied
    discount += item.discount_applied
  print("")
  print(f"SUB TOTAL: $ {total:8.1f} ")
  print(f"DESCUENTO: $ {discount:8.1f} ")
  print(f"IMPUESTO:  $ {tax:8.1f} ")
  print(f"TOTAL:     $ {total - discount + tax:8.1f} ")

if __name__ == "__main__":
  show_invoice(order)