with customers as (

    select
        id as customer_id,
        first_name,
        last_name

    from `julien-test-297518.dbt.customers`

)

select * from customers