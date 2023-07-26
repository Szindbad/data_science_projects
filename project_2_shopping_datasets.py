import codecademylib3
import pandas as pd

visits = pd.read_csv('visits.csv',
                     parse_dates=[1])
cart = pd.read_csv('cart.csv',
                   parse_dates=[1])
checkout = pd.read_csv('checkout.csv',
                       parse_dates=[1])
purchase = pd.read_csv('purchase.csv',
                       parse_dates=[1])

visits_cart_left = pd.merge(visits, cart, how='left')

visits_cart_left_len = len(visits_cart_left)

print(visits_cart_left)

null_rows = pd.isnull(visits_cart_left['cart_time']).sum()

count_null_rows = null_rows.sum()

non_null_rows = ~null_rows
count_non_null_rows = non_null_rows.sum()

visit_no_shop = count_null_rows / (count_null_rows + count_non_null_rows)

visits_cart_left = pd.merge(checkout, cart, how='left')

proportion_non_null = visits_cart_left.count().sum() / visits_cart_left.shape[0]

# Merge visits and cart
visits_cart = pd.merge(visits, cart, how='left')

# Merge visits_cart and checkout
visits_cart_checkout = pd.merge(visits_cart, checkout, how='left')

# Merge visits_cart_checkout and purchase
funnel = pd.merge(visits_cart_checkout, purchase, how='left')

print(funnel.head())

checkout_count = funnel['checkout_time'].notnull().sum()

# Count the number of users who proceeded to checkout but did not make a purchase
checkout_no_purchase_count = (
        funnel['checkout_time'].notnull() &
        funnel['purchase_time'].isnull()
).sum()

checkout_no_purchase_percentage = (checkout_no_purchase_count / checkout_count) * 100

print(checkout_no_purchase_percentage)

# Calculate the completion rates for each step
visit_to_cart_rate = funnel['cart_time'].notnull().mean()
cart_to_checkout_rate = funnel['checkout_time'].notnull().mean()
checkout_to_purchase_rate = funnel['purchase_time'].notnull().mean()
# we can simply print out to see which is the weakest
print(visit_to_cart_rate)
print(cart_to_checkout_rate)
print(checkout_to_purchase_rate)

# or make something useful for later purposes

weakest_step = min(visit_to_cart_rate, cart_to_checkout_rate, checkout_to_purchase_rate)

# Determine the name of the weakest step
if weakest_step == visit_to_cart_rate:
    weakest_step_name = 'Visit to Cart'
elif weakest_step == cart_to_checkout_rate:
    weakest_step_name = 'Cart to Checkout'
else:
    weakest_step_name = 'Checkout to Purchase'

# Print the result
print("The weakest step of the funnel is:", weakest_step_name)

funnel['time_to_purchase'] = \
    funnel.purchase_time - \
    funnel.visit_time

print(funnel.time_to_purchase.mean())
