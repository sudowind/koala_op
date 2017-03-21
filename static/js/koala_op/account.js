/**
 * Created by wangfeng on 2017/3/20.
 */
var account = function () {

    var SCHOOL_ID;
    var CLASS_JOIN_CODE;

    function get_city(province_id) {
        var csrf_token = getCookie('csrftoken');
        $.ajax({
            url: 'get_sub_area/',
            type: 'get',
            data: {
                csrfmiddlewaretoken: csrf_token,
                province_id: province_id
            },
            success: function (data) {
                data = JSON.parse(data);
                var city = [];
                for(var i = 0;i < data.length;i++){
                    city.push({
                        id: data[i].id,
                        text:data[i].regionName
                    });
                }
                $('#city').select2({
                    data: city,
                    language: 'zh-CN'
                });
                get_district($('#city').val());
            }
        })
    }

    function get_district(city_id) {
        var csrf_token = getCookie('csrftoken');
        $.ajax({
            url: 'get_sub_area/',
            type: 'get',
            data: {
                csrfmiddlewaretoken: csrf_token,
                city_id: city_id
            },
            success: function (data) {
                data = JSON.parse(data);
                var district = [];
                for(var i = 0;i < data.length;i++){
                    district.push({
                        id: data[i].regionCode,
                        text:data[i].regionName
                    });
                }
                $('#district').select2({
                    data: district,
                    language: 'zh-CN'
                });
                get_school($('#district').val());
            }
        })
    }

    function get_school(district_id) {
        var csrf_token = getCookie('csrftoken');
        $.ajax({
            url: 'get_sub_area/',
            type: 'get',
            data: {
                csrfmiddlewaretoken: csrf_token,
                district_id: district_id
            },
            success: function (data) {
                data = JSON.parse(data);
                var school = [];
                for(var i = 0;i < data.length;i++){
                    school.push({
                        id: data[i].id,
                        text:data[i].name
                    });
                }
                $('#school').select2({
                    data: school,
                    language: 'zh-CN'
                });
            }
        })
    }

    return {
        init: function () {
            $("#province").on('change',function(){

                $("#city").empty();
                $("#district").empty();
                $("#school").empty();

                get_city($("#province").val());

            });
            $("#city").on('change',function(){

                $("#district").empty();
                $("#school").empty();

                get_district($("#city").val());

            });
            $("#district").on('change',function(){

                $("#school").empty();

                get_school($("#district").val());

            });
            $("#school").on('change',function(){

                D($('#school').val());

            });
        },
        submit_file: function () {
            var csrf_token = getCookie('csrftoken');
            var file = $('#student_file')[0].files[0];
            // D(file);
            var form = new FormData();
            form.append('csrfmiddlewaretoken', csrf_token);
            form.append('file', file);
            D('upload');
            $.ajax({
                url: 'upload/',
                type: 'post',
                data: form,
                processData: false,
                contentType: false,
                success: function (data) {
                    $('#student_table').html(data);
                }
            })
        },
        create_school_master: function () {
            var school_id = $('#school').val();
            SCHOOL_ID = school_id;
            var csrf_token = getCookie('csrftoken');
            $.ajax({
                url: 'create_school_master/',
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    school_id: school_id
                },
                success: function (data) {
                    data = JSON.parse(data);
                    D(data);
                    $('#school_master').html(data['account'] + ' 密码：' + data['psd'])
                }
            })
        },
        create_class: function () {
            // 创建班级老师，创建班级
            var school_id = $('#school').val();
            var grade = $('#grade').val();
            var name = $('#grade option[value=' + grade.toString() + ']').text() + $('#class').val();
            D(name);
            var csrf_token = getCookie('csrftoken');
            $.ajax({
                url: 'create_class/',
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    school_id: school_id,
                    grade: grade,
                    name: name
                },
                success: function (data) {
                    data = JSON.parse(data);
                    D(data);
                    CLASS_JOIN_CODE = data.join_code;
                    $('#class_info').html(data.account + ' ' + data.psd + ' ' + data.join_code);
                }
            })
        },
        create_students: function () {
            var csrf_token = getCookie('csrftoken');
            // D($('#school').val());
            $.ajax({
                url: 'create_students/',
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    school_id: $('#school').val(),
                    join_code: CLASS_JOIN_CODE
                },
                success: function (data) {
                    data = JSON.parse(data);
                    D(data);
                }
            })
        }
    }
}();