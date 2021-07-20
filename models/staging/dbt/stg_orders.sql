with orders as (

    select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

    from `julien-test-297518.dbt.orders`

)

select * from orders