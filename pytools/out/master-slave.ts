export module master-slave {
    export function stages(): any {
        return {
            s100001: {
                id: "s100001",
                name: "东部王国",
                stageNum: 1,
                boss: {
                    id: "e1001",
                    lv: 1,
                },
                reward: [
                    {
                        unit: "gold",
                        value: 10,
                        star: 1,
                    },
                    {
                        unit: "gold",
                        value: 15,
                        star: 2,
                    },
                    {
                        unit: "gold",
                        value: 20,
                        star: 3,
                    },
                ],
            },
            s100002: {
                id: "s100002",
                name: "魔境森林",
                stageNum: 2,
                boss: {
                    id: "e1001",
                    lv: 2,
                },
                reward: [
                    {
                        unit: "gold",
                        value: 25,
                        star: 1,
                    },
                    {
                        unit: "gold",
                        value: 35,
                        star: 2,
                    },
                    {
                        unit: "gold",
                        value: 45,
                        star: 3,
                    },
                ],
            },
            s100003: {
                id: "s100003",
                name: "永歌森林",
                stageNum: 3,
                boss: {
                    id: "e1001",
                    lv: 3,
                },
                reward: [
                    {
                        unit: "gem",
                        value: 50,
                        star: 1,
                    },
                    {
                        unit: "gem",
                        value: 60,
                        star: 2,
                    },
                    {
                        unit: "gem",
                        value: 70,
                        star: 3,
                    },
                ],
            },
        }
    }

    export function foo(): any[] {
        return [
            {
                id: "a",
                arr: [
                    1,
                    2,
                    3,
                ],
            },
            {
                id: "b",
                arr: [
                    2,
                    5,
                ],
            },
            {
                id: "c",
                arr: [
                    3,
                ],
            },
        ]
    }

    export function bar(): any[] {
        return [
            {
                id: "x",
                num: 1,
            },
            {
                id: "y",
                num: 2,
            },
            {
                id: "z",
                num: 3,
            },
        ]
    }

}