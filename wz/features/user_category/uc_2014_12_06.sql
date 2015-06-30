-- 对用户-分类的行为聚集函数
drop table if exists user_category_behavior_agg_2014_12_06;
create table user_category_behavior_agg_2014_12_06 as
select
    -- basic info.
    user_id,
    item_category,
    -- sum
    sum(case when behavior_type=1 then 1 else 0 end) bws_cnt,
    sum(case when behavior_type=2 then 1 else 0 end) clt_cnt,
    sum(case when behavior_type=3 then 1 else 0 end) crt_cnt,
    sum(case when behavior_type=4 then 1 else 0 end) buy_cnt,
    sum(case when behavior_type=2 or behavior_type=3 then 1 else 0 end) clt_crt_cnt,
    count(behavior_type) beh_cnt,
    sum(behavior_type) beh_wgt,
    sum(behavior_type * behavior_type) beh_wgt_pow,
    -- max
    max(case when behavior_type=1 then cast(substr(time, -2) as bigint) else -1 end) max_bws_hr,
    max(case when behavior_type=2 then cast(substr(time, -2) as bigint) else -1 end) max_clt_hr,
    max(case when behavior_type=3 then cast(substr(time, -2) as bigint) else -1 end) max_crt_hr,
    max(case when behavior_type=4 then cast(substr(time, -2) as bigint) else -1 end) max_buy_hr,
    max(cast(substr(time, -2) as bigint)) max_beh_hr,
    -- min
    min(case when behavior_type=1 then cast(substr(time, -2) as bigint) else -1 end) min_bws_hr,
    min(case when behavior_type=2 then cast(substr(time, -2) as bigint) else -1 end) min_clt_hr,
    min(case when behavior_type=3 then cast(substr(time, -2) as bigint) else -1 end) min_crt_hr,
    min(case when behavior_type=4 then cast(substr(time, -2) as bigint) else -1 end) min_buy_hr,
    min(cast(substr(time, -2) as bigint)) min_beh_hr,
    -- span (max - min)
    max(case when behavior_type=1 then cast(substr(time, -2) as bigint) else -1 end) - min(case when behavior_type=1 then cast(substr(time, -2) as bigint) else 0 end) bws_span,
    max(behavior_type) - min(behavior_type) beh_span
from
    mobile_recommend_train_user_filter_item
where
    substr(time, 1, 10) = '2014-12-06'
group by
    user_id, item_category
;
